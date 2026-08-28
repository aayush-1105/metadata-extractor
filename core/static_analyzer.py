import os
import re

def analyze_workspace(repo_path: str) -> dict:
    sloc = 0
    assert_count = 0
    lang_counts = {"java": 0, "python": 0, "ruby": 0}
    
    ignore_dirs = {".git", "node_modules", "venv", ".venv", "__pycache__", "dist", "build"}
    
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext == ".py":
                lang_counts["python"] += 1
            elif ext == ".java":
                lang_counts["java"] += 1
            elif ext == ".rb":
                lang_counts["ruby"] += 1
            else:
                continue
                
            fpath = os.path.join(root, file)
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        line_s = line.strip()
                        if line_s and not line_s.startswith("#") and not line_s.startswith("//"):
                            sloc += 1
                            if "assert" in line_s:
                                assert_count += 1
            except Exception:
                pass
                
    asserts_per_kloc = (assert_count / (sloc / 1000)) if sloc > 0 else 0.0
    
    return {
        "gh_sloc": sloc,
        "gh_asserts_cases_per_kloc": round(asserts_per_kloc, 2),
        "gh_lang_java": 1 if lang_counts["java"] > max(lang_counts["python"], lang_counts["ruby"]) else 0,
        "gh_lang_python": 1 if lang_counts["python"] >= max(lang_counts["java"], lang_counts["ruby"]) and lang_counts["python"] > 0 else 0,
        "gh_lang_ruby": 1 if lang_counts["ruby"] > max(lang_counts["java"], lang_counts["python"]) else 0
    }
