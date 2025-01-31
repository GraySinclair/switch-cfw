import random
from datetime import datetime, timezone, timedelta
import subprocess

# Change these variables -------------------------------
commit_year = 2025
commit_month = 1
commit_day = 31

# Generate random values for hour, minute, second, and microsecond
random_hour = random.randint(7, 22)  # Random hour (0 to 23)
random_minute = random.randint(0, 59)  # Random minute (0 to 59)
random_second = random.randint(0, 59)  # Random second (0 to 59)
#microsecond = random.randint(0, 999999)  # Random microsecond (0 to 999999)

# Create a datetime object with a random time
dt = datetime(commit_year, commit_month, commit_day, random_hour, random_minute, random_second)

# Define the UTC-6 timezone offset (timedelta of -6 hours)
# utc_minus_6 = timezone(timedelta(hours=-6))

# Apply the UTC-6 timezone to the datetime object
# dt_with_timezone = dt.replace(tzinfo=utc_minus_6)

# Convert the datetime object with timezone to a Unix timestamp
# unix_timestamp = dt_with_timezone.timestamp()
unix_timestamp = dt.timestamp()

def get_changed_files():
    subprocess.run(['git', 'reset'])
    subprocess.run(['git', 'add', '.'])
    list_changes = subprocess.run(['git', 'diff', '--name-only', '--cached'], stdout=subprocess.PIPE)
    changed_files = list_changes.stdout.decode('utf-8').strip().split('\n')
    return changed_files if changed_files != [''] else []

def generate_commit_message():
    changed_files = get_changed_files()
    if not changed_files:
        print("No changes detected.")
        return
    
    # Construct the commit message
    commit_message = f"Changes: " + ", ".join(changed_files)
    return commit_message

def main(uts):
    message = generate_commit_message()
    timestamp = str(uts)
    # The Git commit command with the environment variables set
    command = ["git", "commit", "-m", message]
    # Set the GIT_COMMITTER_DATE environment variable and run the command
    # Set the committer's timestamp
    subprocess.run(command, 
    env={
        "GIT_AUTHOR_DATE": timestamp,
        "GIT_COMMITTER_DATE": timestamp,
        "GIT_AUTHOR_NAME": "Gray Sinclair",
        "GIT_AUTHOR_EMAIL": "gray.sinclair@icloud.com",
        "GIT_COMMITTER_NAME": "Gray Sinclair",
        "GIT_COMMITTER_EMAIL": "gray.sinclair@icloud.com"
    }, check=True)
    # push to github
    subprocess.run(['git', 'push', '--force'], check=True)


if __name__ == "__main__":
    main(unix_timestamp)
