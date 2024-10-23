
import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables from.env file
load_dotenv()

# GitHub repository details
repo_owner = 'Coding-Connoisseur'
repo_name = 'AI-Team'
access_token = os.getenv("access_token")

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
    {"title": "Task Prioritization", "tasks": [
        {"description": "Create priority queue system", "due_date": "2024-11-15"},
        {"description": "Dynamically reorder tasks based on urgency", "due_date": "2024-11-22"}
    ]},
    {"title": "System Health and Monitoring", "tasks": [
        {"description": "Track and display agent health", "due_date": "2024-11-10"},
        {"description": "Monitor task success rates", "due_date": "2024-11-17"}
    ]},
    {"title": "Dynamic Thread Management", "tasks": [
        {"description": "Manage dynamic thread pools", "due_date": "2024-11-20"}
    ]},
    {"title": "Testing Automation", "tasks": [
        {"description": "Generate automatic tests based on architecture", "due_date": "2024-11-25"}
    ]},
    {"title": "Failure Handling and Retry Logic", "tasks": [
        {"description": "Implement exponential backoff and retry logic", "due_date": "2024-11-30"}
    ]},
    {"title": "Security Audit", "tasks": [
        {"description": "Perform security audits for common vulnerabilities", "due_date": "2024-12-05"}
    ]},
    {"title": "Task Metadata Storage", "tasks": [
        {"description": "Store task metadata such as execution time and success rates", "due_date": "2024-12-08"}
    ]},
    {"title": "Agent Collaboration and Feedback Loop", "tasks": [
        {"description": "Enable agents to collaborate on complex tasks", "due_date": "2024-12-12"}
    ]},
    {"title": "Documentation Generation", "tasks": [
        {"description": "Generate detailed project documentation", "due_date": "2024-12-18"}
    ]},
    {"title": "User Feedback Integration", "tasks": [
        {"description": "Integrate user feedback to improve system-generated features", "due_date": "2024-12-22"}
    ]},
    {"title": "Advanced Deployment Automation", "tasks": [
        {"description": "Automate deployment with Docker configurations", "due_date": "2024-12-29"}
    ]},
    {"title": "Version Control Integration", "tasks": [
        {"description": "Automatically initialize version control with Git", "due_date": "2025-01-05"}
    ]},
    {"title": "Frontend and Backend Integration", "tasks": [
        {"description": "Generate frontend structure with sample HTML and CSS", "due_date": "2025-01-12"}
    ]},
    {"title": "Error Handling and Logging", "tasks": [
        {"description": "Implement comprehensive logging and error handling", "due_date": "2025-01-19"}
    ]}
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
