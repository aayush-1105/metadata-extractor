import subprocess
import json
from datetime import datetime

def gh_cli_json(endpoint: str):
    cmd = f"gh api {endpoint}"
    res = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    if res.returncode == 0:
        try:
            return json.loads(res.stdout)
        except Exception:
            return None
    return None

def get_github_metadata(owner: str, repo: str, commit_sha: str) -> dict:
    metrics = {
        "gh_project_name": f"{owner}/{repo}",
        "gh_is_pr": 0,
        "gh_pull_req_num": 0,
        "gh_pr_created_at_year": 0,
        "gh_pr_created_at_month": 0,
        "gh_description_complexity": 0,
        "gh_num_pr_comments": 0,
        "gh_num_issue_comments": 0,
        "gh_num_commit_comments": 0,
        "gh_team_size": 1,
        "gh_by_core_team_member": 1,
        "gh_pushed_at": ""
    }
    
    prs = gh_cli_json(f"repos/{owner}/{repo}/commits/{commit_sha}/pulls")
    if prs and isinstance(prs, list) and len(prs) > 0:
        pr = prs[0]
        metrics["gh_is_pr"] = 1
        metrics["gh_pull_req_num"] = pr.get("number", 0)
        body = pr.get("body") or ""
        metrics["gh_description_complexity"] = len(body.split())
        metrics["gh_num_pr_comments"] = pr.get("comments", 0) + pr.get("review_comments", 0)
        
        created_at = pr.get("created_at")
        if created_at:
            dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            metrics["gh_pr_created_at_year"] = dt.year
            metrics["gh_pr_created_at_month"] = dt.month

    commit_data = gh_cli_json(f"repos/{owner}/{repo}/commits/{commit_sha}")
    if commit_data:
        metrics["gh_num_commit_comments"] = commit_data.get("commit", {}).get("comment_count", 0)
        metrics["gh_pushed_at"] = commit_data.get("commit", {}).get("author", {}).get("date", "")

    contributors = gh_cli_json(f"repos/{owner}/{repo}/contributors")
    if contributors and isinstance(contributors, list):
        metrics["gh_team_size"] = len(contributors)
        
    return metrics
