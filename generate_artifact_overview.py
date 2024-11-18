import requests
import argparse
import json
from datetime import datetime

def get_repositories(org, headers):
    """Fetch all repositories in the organization."""
    repos = []
    url = f"https://api.github.com/orgs/{org}/repos"
    while url:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        repos.extend(response.json())
        url = response.links.get("next", {}).get("url")  # Handle pagination
    return repos

def get_artifacts(owner, repo, headers):
    """Fetch all artifacts for a specific repository."""
    artifacts = []
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/artifacts"
    while url:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        artifacts.extend(response.json().get("artifacts", []))
        url = response.links.get("next", {}).get("url")  # Handle pagination
    return artifacts

def human_readable_size(size_in_bytes):
    """Convert size in bytes to a human-readable format (MB or GB)."""
    if size_in_bytes >= 1e9:
        return f"{size_in_bytes / 1e9:.2f} GB"
    return f"{size_in_bytes / 1e6:.2f} MB"

def is_expired(expiry_date):
    """Check if an artifact has expired."""
    now = datetime.utcnow()
    expires_at = datetime.strptime(expiry_date, "%Y-%m-%dT%H:%M:%SZ")
    return now > expires_at

def main(org, token, ignore_expired):
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }
    
    print(f"Fetching repositories for organization: {org}")
    repos = get_repositories(org, headers)
    
    overview = {}
    total_size = 0  # Keep track of total size of all artifacts
    
    for repo in repos:
        repo_name = repo["name"]
        print(f"Fetching artifacts for repository: {repo_name}")
        artifacts = get_artifacts(org, repo_name, headers)
        
        if artifacts:
            repo_artifacts = []
            for artifact in artifacts:
                if ignore_expired and is_expired(artifact["expires_at"]):
                    print(f"  Skipping expired artifact: {artifact['name']}")
                    continue
                
                artifact_info = {
                    "name": artifact["name"],
                    "size_in_bytes": artifact["size_in_bytes"],
                    "created_at": artifact["created_at"],
                    "expires_at": artifact["expires_at"],
                    "workflow_run_id": artifact["workflow_run"]["id"]
                }
                repo_artifacts.append(artifact_info)
                total_size += artifact["size_in_bytes"]
            if repo_artifacts:
                overview[repo_name] = repo_artifacts
    
    # Print the grouped overview
    print("\n=== Artifacts Overview ===")
    for repo_name, artifacts in overview.items():
        print(f"\nRepository: {repo_name}")
        for artifact in artifacts:
            print(f"  - Artifact: {artifact['name']}, Size: {human_readable_size(artifact['size_in_bytes'])}")
            print(f"    Created: {artifact['created_at']}, Expires: {artifact['expires_at']}")
            print(f"    Workflow Run ID: {artifact['workflow_run_id']}")
    
    # Print the total size of all artifacts
    print(f"\nTotal size of all artifacts: {human_readable_size(total_size)}")
    
    # Save the overview to a file
    with open("artifacts_overview.json", "w") as f:
        json.dump(overview, f, indent=4)
    print("\nOverview saved to artifacts_overview.json")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch GitHub artifacts grouped by repository.")
    parser.add_argument("organization", type=str, help="GitHub organization name")
    parser.add_argument("token", type=str, help="GitHub Personal Access Token")
    parser.add_argument("--ignore-expired", action="store_true", help="Ignore expired artifacts")
    args = parser.parse_args()

    main(args.organization, args.token, args.ignore_expired)
