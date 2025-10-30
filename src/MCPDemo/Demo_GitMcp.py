from fastapi import FastAPI
import requests

app = FastAPI(title="Local MCP Server - GitHub Demo")

# Configuration for your GitHub public repo
GITHUB_API = "https://api.github.com"
REPO_OWNER = "S158984"
REPO_NAME = "Flask"

@app.get("/")
def root():
    """Root endpoint - health check"""
    return {"message": "✅ MCP GitHub Server is running!"}

@app.get("/repo/info")
def get_repo_info():
    """Fetch basic repository information"""
    url = f"{GITHUB_API}/repos/{REPO_OWNER}/{REPO_NAME}"
    response = requests.get(url)
    return response.json()

@app.get("/repo/branches")
def get_branches():
    """List all branches in the repository"""
    url = f"{GITHUB_API}/repos/{REPO_OWNER}/{REPO_NAME}/branches"
    response = requests.get(url)
    return response.json()

@app.get("/repo/commits")
def get_commits(limit: int = 5):
    """Fetch latest commits from the repository"""
    url = f"{GITHUB_API}/repos/{REPO_OWNER}/{REPO_NAME}/commits"
    response = requests.get(url)
    commits = response.json()
    simplified = [
        {
            "sha": c["sha"],
            "author": c["commit"]["author"]["name"],
            "message": c["commit"]["message"],
            "date": c["commit"]["author"]["date"]
        }
        for c in commits[:limit]
    ]
    return simplified

