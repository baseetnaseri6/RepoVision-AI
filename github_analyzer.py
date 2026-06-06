import os
import base64
from collections import Counter
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def parse_github_url(repo_url):
    repo_url = repo_url.strip()
    parsed_url = urlparse(repo_url)

    if parsed_url.netloc != "github.com":
        raise ValueError("Please enter a valid GitHub repository URL.")

    parts = parsed_url.path.strip("/").split("/")

    if len(parts) < 2:
        raise ValueError("Invalid GitHub repository URL format.")

    return parts[0], parts[1]


def github_headers():
    headers = {"Accept": "application/vnd.github+json"}

    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    return headers


def github_get(url):
    response = requests.get(url, headers=github_headers(), timeout=15)

    if response.status_code == 403:
        raise Exception("GitHub API limit reached. Add your GitHub token in .env.")

    return response


def get_repo_contents(owner, repo, path=""):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    response = github_get(url)

    if response.status_code != 200:
        return []

    data = response.json()

    if not isinstance(data, list):
        return []

    return data


def count_api_items(url):
    response = github_get(url)

    if response.status_code != 200:
        return 0

    data = response.json()

    if isinstance(data, list):
        return len(data)

    return 0


def get_owner_profile(owner):
    url = f"https://api.github.com/users/{owner}"
    response = github_get(url)

    if response.status_code != 200:
        return {
            "followers": 0,
            "following": 0,
            "public_repos": 0,
            "bio": "No bio available",
            "location": "Unknown",
        }

    data = response.json()

    return {
        "followers": data.get("followers", 0),
        "following": data.get("following", 0),
        "public_repos": data.get("public_repos", 0),
        "bio": data.get("bio") or "No bio available",
        "location": data.get("location") or "Unknown",
    }


def get_readme_preview(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    response = github_get(url)

    if response.status_code != 200:
        return "README preview is not available."

    data = response.json()
    content = data.get("content", "")

    try:
        decoded = base64.b64decode(content).decode("utf-8", errors="ignore")
        lines = decoded.splitlines()
        clean_lines = [line.strip() for line in lines if line.strip()]
        preview = "\n".join(clean_lines[:12])
        return preview if preview else "README preview is empty."
    except Exception:
        return "README preview could not be decoded."


def get_last_commit(owner, repo, default_branch):
    url = f"https://api.github.com/repos/{owner}/{repo}/commits/{default_branch}"
    response = github_get(url)

    if response.status_code != 200:
        return "Unknown"

    data = response.json()

    return (
        data.get("commit", {})
        .get("committer", {})
        .get("date", "Unknown")
    )


def get_top_contributors(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/contributors?per_page=5"
    response = github_get(url)

    if response.status_code != 200:
        return []

    contributors = []

    for item in response.json():
        contributors.append({
            "username": item.get("login", "Unknown"),
            "avatar_url": item.get("avatar_url", ""),
            "contributions": item.get("contributions", 0),
            "html_url": item.get("html_url", "#"),
        })

    return contributors


def get_activity_data(owner, repo):
    commits = count_api_items(
        f"https://api.github.com/repos/{owner}/{repo}/commits?per_page=100"
    )

    issues = count_api_items(
        f"https://api.github.com/repos/{owner}/{repo}/issues?state=all&per_page=100"
    )

    pulls = count_api_items(
        f"https://api.github.com/repos/{owner}/{repo}/pulls?state=all&per_page=100"
    )

    return {
        "labels": ["Commits", "Issues", "Pull Requests"],
        "values": [commits, issues, pulls],
    }


def get_repo_data(repo_url):
    owner, repo = parse_github_url(repo_url)

    repo_api = f"https://api.github.com/repos/{owner}/{repo}"
    repo_response = github_get(repo_api)

    if repo_response.status_code == 404:
        raise Exception("Repository not found. Please check the URL.")

    if repo_response.status_code != 200:
        raise Exception("GitHub API error. Please try again.")

    repo_data = repo_response.json()
    root_contents = get_repo_contents(owner, repo)

    files = []
    file_extensions = []

    for item in root_contents:
        name = item.get("name", "")

        if item.get("type") == "file":
            files.append(name)

            if "." in name:
                file_extensions.append(name.split(".")[-1].lower())
            else:
                file_extensions.append("other")

        if item.get("type") == "dir":
            files.append(name)

    owner_data = repo_data.get("owner", {})
    default_branch = repo_data.get("default_branch", "main")
    license_data = repo_data.get("license")
    contributors = get_top_contributors(owner, repo)

    return {
        "name": repo_data.get("name", "Unknown"),
        "full_name": repo_data.get("full_name", "Unknown"),
        "description": repo_data.get("description") or "No description available",
        "language": repo_data.get("language") or "Unknown",
        "stars": repo_data.get("stargazers_count", 0),
        "forks": repo_data.get("forks_count", 0),
        "watchers": repo_data.get("watchers_count", 0),
        "open_issues": repo_data.get("open_issues_count", 0),
        "size": repo_data.get("size", 0),
        "created_at": repo_data.get("created_at", "Unknown"),
        "updated_at": repo_data.get("updated_at", "Unknown"),
        "last_commit": get_last_commit(owner, repo, default_branch),
        "default_branch": default_branch,
        "license": license_data.get("name") if license_data else "No license",
        "contributors": len(contributors),
        "contributors_list": contributors,
        "owner_profile": get_owner_profile(owner),
        "readme_preview": get_readme_preview(owner, repo),
        "open_pull_requests": count_api_items(
            f"https://api.github.com/repos/{owner}/{repo}/pulls?state=open"
        ),
        "releases": count_api_items(
            f"https://api.github.com/repos/{owner}/{repo}/releases"
        ),
        "html_url": repo_data.get("html_url", repo_url),
        "avatar_url": owner_data.get("avatar_url", ""),
        "owner": owner_data.get("login", "Unknown"),
        "files": files,
        "file_extensions": file_extensions,
        "activity_data": get_activity_data(owner, repo),
    }


def calculate_scores(repo):
    documentation = 45
    code_quality = 50
    security = 55
    health = 50

    files = repo.get("files", [])

    has_readme = "README.md" in files or "readme.md" in files
    has_dependencies = (
        "requirements.txt" in files
        or "pyproject.toml" in files
        or "package.json" in files
    )
    has_gitignore = ".gitignore" in files

    if has_readme:
        documentation += 35

    if repo["description"] != "No description available":
        documentation += 15

    if has_dependencies:
        code_quality += 20

    if has_gitignore:
        code_quality += 12
        security += 15

    if repo["license"] != "No license":
        documentation += 5
        health += 5

    if repo["stars"] >= 50:
        health += 8

    if repo["stars"] >= 500:
        health += 8

    if repo["forks"] >= 50:
        health += 7

    if repo["contributors"] >= 5:
        health += 8

    if repo["releases"] >= 1:
        health += 6

    if repo["open_issues"] > 50:
        health -= 8

    documentation = min(max(documentation, 0), 100)
    code_quality = min(max(code_quality, 0), 100)
    security = min(max(security, 0), 100)
    health = min(max(health, 0), 100)

    overall = int((documentation + code_quality + security + health) / 4)

    return {
        "overall": overall,
        "code_quality": code_quality,
        "security": security,
        "documentation": documentation,
        "health": health,
    }


def detect_technologies(repo):
    files = repo.get("files", [])
    language = repo.get("language", "Unknown")
    technologies = []

    if language and language != "Unknown":
        technologies.append(language)

    if "requirements.txt" in files or "pyproject.toml" in files:
        technologies.append("Python")

    if "package.json" in files:
        technologies.append("Node.js")

    if "Dockerfile" in files or "docker-compose.yml" in files:
        technologies.append("Docker")

    if ".github" in files:
        technologies.append("GitHub Actions")

    if "manage.py" in files:
        technologies.append("Django")

    if "app.py" in files or "flask_app.py" in files:
        technologies.append("Flask")

    if "vite.config.js" in files or "vite.config.ts" in files:
        technologies.append("Vite")

    if "tailwind.config.js" in files or "tailwind.config.ts" in files:
        technologies.append("Tailwind CSS")

    clean_list = []

    for tech in technologies:
        if tech not in clean_list:
            clean_list.append(tech)

    return clean_list[:8]


def calculate_ai_readiness(repo, scores, technologies):
    readiness = 40
    files = repo.get("files", [])

    if "README.md" in files or "readme.md" in files:
        readiness += 15

    if ".gitignore" in files:
        readiness += 10

    if repo.get("license") != "No license":
        readiness += 10

    if "Dockerfile" in files:
        readiness += 10

    if ".github" in files:
        readiness += 10

    if repo.get("contributors", 0) > 0:
        readiness += 5

    if scores["overall"] >= 75:
        readiness += 10

    readiness = min(readiness, 100)

    if readiness >= 80:
        level = "High"
    elif readiness >= 60:
        level = "Medium"
    else:
        level = "Low"

    return {
        "score": readiness,
        "level": level,
        "checks": [
            "Documentation checked",
            "Repository structure scanned",
            "Security signals reviewed",
            "Technology stack detected",
        ],
    }


def generate_risk_analysis(repo, issues):
    high_count = len([item for item in issues if item[2] == "high"])
    medium_count = len([item for item in issues if item[2] == "medium"])

    if high_count > 0:
        level = "High Risk"
        color = "high"
    elif medium_count > 1:
        level = "Medium Risk"
        color = "medium"
    else:
        level = "Low Risk"
        color = "low"

    return {
        "level": level,
        "color": color,
        "points": [
            "Repository metadata reviewed",
            "Security basics checked",
            "Documentation status checked",
            "Dependency signals checked",
        ],
    }


def generate_issues(repo):
    files = repo.get("files", [])
    issues = []

    if "README.md" not in files and "readme.md" not in files:
        issues.append(("Missing README.md file", "High", "high"))

    if ".gitignore" not in files:
        issues.append(("Missing .gitignore file", "Medium", "medium"))

    if (
        "requirements.txt" not in files
        and "pyproject.toml" not in files
        and "package.json" not in files
    ):
        issues.append(("Missing dependency file", "Medium", "medium"))

    if repo["license"] == "No license":
        issues.append(("Missing open-source license", "Medium", "medium"))

    if repo["description"] == "No description available":
        issues.append(("Missing repository description", "Low", "low"))

    if repo["open_issues"] > 50:
        issues.append(("Too many open issues", "High", "high"))

    if repo["contributors"] == 0:
        issues.append(("No contributors detected", "Low", "low"))

    if not issues:
        issues.append(("No major issues detected", "Low", "low"))

    return issues


def generate_recommendations(repo):
    files = repo.get("files", [])
    recommendations = []

    if "README.md" not in files and "readme.md" not in files:
        recommendations.append("Add a professional README with setup, usage, screenshots and examples.")

    if ".gitignore" not in files:
        recommendations.append("Add a .gitignore file to avoid uploading cache, environment and system files.")

    if (
        "requirements.txt" not in files
        and "pyproject.toml" not in files
        and "package.json" not in files
    ):
        recommendations.append("Add requirements.txt, pyproject.toml or package.json for dependency management.")

    if repo["license"] == "No license":
        recommendations.append("Add a license so other developers know how they can use your project.")

    if repo["description"] == "No description available":
        recommendations.append("Add a clear GitHub repository description.")

    if repo["releases"] == 0:
        recommendations.append("Create releases or version tags to make the project look more production-ready.")

    recommendations.append("Use environment variables for API keys and secrets.")
    recommendations.append("Add unit tests to improve project reliability.")

    return recommendations


def generate_ai_summary(repo, scores, issues, recommendations):
    strengths = []
    weaknesses = []

    if scores["documentation"] >= 75:
        strengths.append("Good documentation signals are detected.")
    else:
        weaknesses.append("Documentation needs improvement.")

    if scores["code_quality"] >= 75:
        strengths.append("Project structure and dependency signals look healthy.")
    else:
        weaknesses.append("Code quality can be improved with better structure and dependency files.")

    if scores["security"] >= 75:
        strengths.append("Basic security setup looks acceptable.")
    else:
        weaknesses.append("Security setup should be improved, especially around .gitignore and secret handling.")

    if scores["health"] >= 75:
        strengths.append("Repository health looks strong based on GitHub activity signals.")
    else:
        weaknesses.append("Repository health could improve with more activity, contributors, releases and issue management.")

    summary = (
        f"{repo.get('full_name', 'This repository')} is mainly a "
        f"{repo.get('language', 'software')} project. "
        f"It received an overall score of {scores['overall']}/100. "
        f"The dashboard detected repository structure, documentation, security signals, "
        f"GitHub activity and improvement opportunities."
    )

    return {
        "summary": summary,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "next_steps": recommendations[:4],
    }


def generate_file_distribution(repo):
    extensions = repo.get("file_extensions", [])

    if not extensions:
        return ["No Data"], [0]

    counter = Counter(extensions)

    extension_map = {
        "py": "Python",
        "md": "Markdown",
        "js": "JavaScript",
        "ts": "TypeScript",
        "html": "HTML",
        "css": "CSS",
        "json": "JSON",
        "txt": "Text",
        "yml": "YAML",
        "yaml": "YAML",
        "toml": "TOML",
        "env": "ENV",
        "csv": "CSV",
    }

    labels = []
    values = []

    total = sum(counter.values())

    for ext, count in counter.most_common(6):
        labels.append(extension_map.get(ext, ext.upper()))
        values.append(round((count / total) * 100, 1))

    return labels, values