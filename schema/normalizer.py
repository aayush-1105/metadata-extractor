import pandas as pd
from schema.columns import COLUMNS

def normalize_features(data_dict: dict) -> pd.DataFrame:
    row = {}
    for col in COLUMNS:
        val = data_dict.get(col, None)
        if val is None:
            if col.startswith("gh_lang_") or col.startswith("git_prev_commit_resolution_status_") or col in ["gh_is_pr", "gh_by_core_team_member", "target_binary"]:
                row[col] = 0
            elif "num" in col or "churn" in col or "files" in col or "sloc" in col or "age" in col or "duration" in col or "year" in col or "month" in col or "density" in col or "kloc" in col:
                row[col] = 0
            else:
                row[col] = ""
        else:
            row[col] = val
    df = pd.DataFrame([row], columns=COLUMNS)
    return df
