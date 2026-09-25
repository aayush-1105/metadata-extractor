# Repository Metadata Feature Extractor

Extracts 39 TravisTorrent-aligned metadata features from any GitHub repository commit for ML build failure prediction.

## Usage
```powershell
python main.py --repo https://github.com/pallets/flask --output features.csv
```

By default it extracts the latest commit on `main` and **appends** a row to the
output CSV. Options:

| Flag | Default | Description |
|------|---------|-------------|
| `--repo` | (required) | GitHub URL or local path |
| `--branch` | `main` | Branch to read commits from |
| `-n`, `--num-commits` | `1` | Number of most-recent commits to extract (one row each) |
| `--commit` | branch tip | Start from a specific commit instead of the branch tip |
| `--write-mode` | `append` | `append` to the CSV or `overwrite` it |
| `--output` | `features.csv` | Output CSV path |

Examples:
```powershell
# last 10 commits on main, appended to the CSV
python main.py --repo https://github.com/pallets/flask -n 10

# last 5 commits on a different branch, replacing the file
python main.py --repo https://github.com/pallets/flask --branch develop -n 5 --write-mode overwrite
```

Each target commit is checked out so static-analysis features reflect that
commit's tree (skipped with a warning for a local repo that has uncommitted
changes).

