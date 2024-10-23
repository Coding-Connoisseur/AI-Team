
import requests
from datetime import datetime, timedelta

# GitHub repository details
repo_owner = 'Coding-Connoisseur'
repo_name = 'AI-Team'
access_token = 'your_github_token'  # Replace with a valid GitHub token

# GitHub API URL for creating issues
issues_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/issues'

# Sample user stories
user_stories = [
    {"title": "Agent Enhancement and Learning", "tasks": [
        {"description": "Implement success rate tracking for agents", "due_date": "2024-11-01"},
        {"description": "Enable agents to adjust behavior based on success rates", "due_date": "2024-11-07"}
    ]},
    {"title": "Project Setup", "tasks": [
        {"description": "Allow users to specify project type", "due_date": "2024-11-03"},
        {"description": "Dynamically create architecture based on project type", "due_date": "2024-11-10"}
    ]},
    # Additional stories here...
]

# Headers for GitHub API request
headers = {
    'Authorization': f'token {access_token}',
    'Accept': 'application/vnd.github.v3+json'
}

def create_github_issue(title, body):
    """Creates an issue on GitHub."""
    issue_data = {
        'title': title,
        'body': body
    }
    response = requests.post(issues_url, json=issue_data, headers=headers)
    if response.status_code == 201:
        print(f"Issue '{title}' created successfully!")
    else:
        print(f"Failed to create issue '{title}'. Status Code: {response.status_code}, Response: {response.json()}")

def main():
    for story in user_stories:
        # Create the main issue for each user story
        title = story['title']
        body = f"**User Story**: {title}\n\n**Tasks**:\n"
        for task in story['tasks']:
            due_date = task['due_date']
            body += f"- {task['description']} (Due: {due_date})\n"

        create_github_issue(title, body)

if __name__ == "__main__":
    main()
