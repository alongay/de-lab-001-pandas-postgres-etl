import os
from datetime import datetime, timedelta

def check_delta_freshness(delta_path, max_age_minutes=5):
    """
    Checks if a Delta table has been updated within the last N minutes.
    Returns (is_fresh, age_minutes, latest_commit_file)
    """
    delta_log_path = os.path.join(delta_path, "_delta_log")
    if not os.path.exists(delta_log_path):
        return False, None, None

    # Get all .json files (commits)
    commits = [f for f in os.listdir(delta_log_path) if f.endswith('.json')]
    if not commits:
        return False, None, None

    # Get the latest commit
    latest_commit = sorted(commits)[-1]
    latest_commit_path = os.path.join(delta_log_path, latest_commit)
    
    mtime = os.path.getmtime(latest_commit_path)
    last_modified = datetime.fromtimestamp(mtime)
    age = datetime.now() - last_modified
    age_minutes = age.total_seconds() / 60

    return age_minutes <= max_age_minutes, age_minutes, latest_commit

def verify_audit_artifact(artifact_path):
    """
    Verifies the existence of a quality audit artifact (e.g., GE JSON).
    """
    return os.path.exists(artifact_path)
