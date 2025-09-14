import requests
import re
from datetime import datetime, timezone

REPOS = {
    "RETAILEASE": "ronnydrooid/RetailEase",
}

README_FILE = "README.md"

def days_ago(iso_date):
    commit_time = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))
    diff = datetime.now(timezone.utc) - commit_time
    days = diff.days
    if days == 0:
        return "today"
    elif days == 1:
        return "1 day ago"
    return f"{days} days ago"

def get_last_commit(repo):
    url = f"https://api.github.com/repos/{repo}/commits"
    r = requests.get(url)
    r.raise_for_status()
    commit = r.json()[0]
    return commit["commit"]["committer"]["date"]

def update_readme():
    with open(README_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    for key, repo in REPOS.items():
        last_commit = get_last_commit(repo)
        ago = days_ago(last_commit)
        placeholder = f"<!--{key}_COMMIT-->"
        content = re.sub(f"{placeholder}", ago, content)

    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    update_readme()
