from fastapi import FastAPI
from git import Repo
from pathlib import Path
import os

# Path to your cloned repo
REPO_PATH = Path("D:\Datascience\MLProject\Flask")  # 🔁 change this to your local path
if not REPO_PATH.exists():
    raise FileNotFoundError(f"Repository not found at {REPO_PATH}")

repo = Repo(REPO_PATH)
app = FastAPI(title="GitHub MCP Server")

@app.get("/")
def root():
    return {"message": "MCP Git Server is running"}

@app.get("/branches")
def list_branches():
    branches = [head.name for head in repo.heads]
    return {"branches": branches}

@app.get("/commits/{branch_name}")
def list_commits(branch_name: str, limit: int = 5):
    try:
        commits = list(repo.iter_commits(branch_name, max_count=limit))
        return {
            "branch": branch_name,
            "commits": [
                {
                    "hexsha": c.hexsha,
                    "message": c.message.strip(),
                    "author": c.author.name,
                    "date": c.committed_datetime.isoformat()
                }
                for c in commits
            ]
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/files")
def list_files():
    files = [str(p) for p in REPO_PATH.rglob("*") if p.is_file()]
    return {"total_files": len(files), "files": files[:50]}  # limit preview

@app.get("/filecontent")
def get_file_content(filepath: str):
    try:
        full_path = REPO_PATH / filepath
        if not full_path.exists():
            return {"error": "File not found"}
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
        return {"file": filepath, "content": content}
    except Exception as e:
        return {"error": str(e)}