import os
import sys
import argparse
import subprocess
import shutil

from core.git_engine import get_churn_metrics, get_repo_git_metrics
from core.static_analyzer import analyze_workspace
from core.github_api import get_github_metadata
from core.ci_analyzer import get_ci_metrics
from schema.normalizer import normalize_features

def parse_repo_url(url: str):
    clean = url.rstrip("/").replace(".git", "")
    parts = clean.split("/")
    return parts[-2], parts[-1]

def main():
    parser = argparse.ArgumentParser(description="Extract 51 TravisTorrent Metadata Features from a Repository")
    parser.add_argument("--repo", type=str, required=True, help="GitHub repository URL or local path")
    parser.add_argument("--commit", type=str, default=None, help="Commit SHA (defaults to HEAD)")
    parser.add_argument("--output", type=str, default="features.csv", help="Output CSV path")
    args = parser.parse_args()

    temp_dir = None
    if args.repo.startswith("http://") or args.repo.startswith("https://"):
        owner, repo = parse_repo_url(args.repo)
        temp_dir = os.path.join(os.getcwd(), "temp_target_repo")
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)
        print(f"[*] Cloning {args.repo} into temporary workspace...")
        subprocess.run(f"git clone {args.repo} {temp_dir}", shell=True, check=True)
        repo_path = temp_dir
    else:
        repo_path = os.path.abspath(args.repo)
        owner, repo = "local", os.path.basename(repo_path)

    try:
        commit_sha = args.commit
        if not commit_sha:
            res = subprocess.run("git rev-parse HEAD", cwd=repo_path, capture_output=True, text=True, shell=True)
            commit_sha = res.stdout.strip()

        print(f"[*] Extracting features for Repo: {owner}/{repo} | Commit: {commit_sha}...")
        
        all_features = {}
        all_features.update(get_churn_metrics(repo_path, commit_sha))
        all_features.update(get_repo_git_metrics(repo_path, commit_sha))
        all_features.update(analyze_workspace(repo_path))
        all_features.update(get_github_metadata(owner, repo, commit_sha))
        all_features.update(get_ci_metrics(owner, repo, commit_sha))

        df = normalize_features(all_features)
        
        output_path = os.path.abspath(args.output)
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
        df.to_csv(output_path, index=False)
        
        print(f"[+] Successfully extracted {df.shape[1]} features to {output_path}")
        print(df.T)
    finally:
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    main()
