from crewai.tools import BaseTool
import requests
import os
from typing import Type
from pydantic import BaseModel, Field

class GitHubAnalysisInput(BaseModel):
    """Input schema for GitHub analysis."""
    repository: str = Field(..., description="Repository in 'owner/repo' format (e.g., 'facebook/react')")

class MCPGitHubTool(BaseTool):
    name: str = "GitHub Repository Analyzer"
    description: str = "Analyze a GitHub repository and get health metrics: stars, forks, issues, recent commits, contributors, etc."
    args_schema: Type[BaseModel] = GitHubAnalysisInput
    
    def _run(self, repository: str) -> str:
        """Analyze GitHub repository."""
        try:
            token = os.getenv('GITHUB_TOKEN')
            headers = {
                'Authorization': f'token {token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            # Get repo info
            repo_url = f"https://api.github.com/repos/{repository}"
            repo_response = requests.get(repo_url, headers=headers, timeout=30)
            repo_response.raise_for_status()
            repo_data = repo_response.json()
            
            # Get recent commits
            commits_url = f"{repo_url}/commits"
            commits_response = requests.get(commits_url, headers=headers, params={'per_page': 10}, timeout=30)
            commits_data = commits_response.json() if commits_response.status_code == 200 else []
            
            # Get issues
            issues_url = f"{repo_url}/issues"
            open_issues = requests.get(issues_url, headers=headers, params={'state': 'open', 'per_page': 1}, timeout=30)
            closed_issues = requests.get(issues_url, headers=headers, params={'state': 'closed', 'per_page': 1}, timeout=30)
            
            # Format results
            analysis = f"""
REPOSITORY ANALYSIS: {repository}

📊 GENERAL METRICS:
- Stars: {repo_data.get('stargazers_count', 0):,}
- Forks: {repo_data.get('forks_count', 0):,}
- Watchers: {repo_data.get('watchers_count', 0):,}
- Open Issues: {repo_data.get('open_issues_count', 0):,}
- Main Language: {repo_data.get('language', 'N/A')}
- Created: {repo_data.get('created_at', 'N/A')[:10]}
- Last Update: {repo_data.get('updated_at', 'N/A')[:10]}
- Last Push: {repo_data.get('pushed_at', 'N/A')[:10]}

📈 ACTIVITY:
- Recent Commits: {len(commits_data)} commits in latest records
- License: {repo_data.get('license', {}).get('name', 'Not specified') if repo_data.get('license') else 'Not specified'}
- Description: {repo_data.get('description', 'No description')}

🔗 URL: {repo_data.get('html_url', 'N/A')}
"""
            return analysis
            
        except requests.exceptions.RequestException as e:
            return f"Error analyzing repository: {str(e)}"