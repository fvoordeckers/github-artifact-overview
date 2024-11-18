# Github Artifact Overview generator
Generates an overview of all artifacts within an organization.

### **How to Run the Script**

#### Include Expired Artifacts (Default):
```bash
python generate_artifact_overview.py setlebe your_github_token
```

#### Ignore Expired Artifacts:
```bash
python generate_artifact_overview.py setlebe your_github_token --ignore-expired
```

---

### **Sample Output**
#### Console:
```text
Fetching artifacts for repository: repo1
  Skipping expired artifact: old_logs

Fetching artifacts for repository: repo2

=== Artifacts Overview ===

Repository: repo2
  - Artifact: test_results, Size: 20.48 MB
    Created: 2024-11-05T08:00:00Z, Expires: 2024-12-05T08:00:00Z
    Workflow Run ID: 987654321

Total size of all artifacts: 20.48 MB
```

#### File (`artifacts_overview.json`):
```json
{
    "repo2": [
        {
            "name": "test_results",
            "size_in_bytes": 20480000,
            "created_at": "2024-11-05T08:00:00Z",
            "expires_at": "2024-12-05T08:00:00Z",
            "workflow_run_id": 987654321
        }
    ]
}
```

---

Let me know if you need further adjustments!