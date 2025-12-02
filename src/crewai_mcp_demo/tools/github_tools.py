"""
Custom tools to interact with the GitHub API
They replace the functionalities of GitHub's MCP
"""
import os
import requests
from crewai.tools import BaseTool

class GitHubRepoTool(BaseTool):
    name: str = "Get GitHub Repository Info"
    description: str = "Retrieves detailed information about a GitHub repository (stars, forks, issues, etc.)"
    
    def _run(self, repo_full_name: str) -> str:
        """
        Retrieves information about a repository
        Args:
            repo_full_name: Full name of the repo (e.g., 'owner/repo')
        """
        token = os.getenv("GITHUB_API_KEY")
        headers = {"Authorization": f"token {token}"} if token else {}
        
        try:
            url = f"https://api.github.com/repos/{repo_full_name}"
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return f"""
            Repository: {data['full_name']}
            Description: {data.get('description', 'N/A')}
            Stars: {data['stargazers_count']}
            Forks: {data['forks_count']}
            Open Issues: {data['open_issues_count']}
            Language: {data.get('language', 'N/A')}
            Created: {data['created_at']}
            Updated: {data['updated_at']}
            License: {data.get('license', {}).get('name', 'N/A')}
            URL: {data['html_url']}
            """
        except Exception as e:
            return f"Error retrieving repository: {str(e)}"


class GitHubCommitsTool(BaseTool):
    name: str = "List GitHub Commits"
    description: str = "Lists the latest commits of a GitHub repository"
    
    def _run(self, repo_full_name: str, limit: int = 10) -> str:
        """
        Lists recent commits
        Args:
            repo_full_name: Full name of the repo (e.g., 'owner/repo')
            limit: Maximum number of commits to retrieve (default: 10)
        """
        token = os.getenv("GITHUB_API_KEY")
        headers = {"Authorization": f"token {token}"} if token else {}
        
        try:
            url = f"https://api.github.com/repos/{repo_full_name}/commits"
            params = {"per_page": min(limit, 100)}
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            commits = response.json()
            result = f"Last {len(commits)} commits for {repo_full_name}:\n\n"
            
            for commit in commits[:limit]:
                sha = commit['sha'][:7]
                message = commit['commit']['message'].split('\n')[0]
                author = commit['commit']['author']['name']
                date = commit['commit']['author']['date']
                result += f"- {sha}: {message} (by {author} on {date})\n"
            
            return result
        except Exception as e:
            return f"Error retrieving commits: {str(e)}"


class GitHubIssuesTool(BaseTool):
    name: str = "List GitHub Issues"
    description: str = "Lists open or closed issues of a GitHub repository"
    
    def _run(self, repo_full_name: str, state: str = "open", limit: int = 10) -> str:
        """
        Lists repository issues
        Args:
            repo_full_name: Full name of the repo (e.g., 'owner/repo')
            state: Issue state: 'open', 'closed', 'all' (default: 'open')
            limit: Maximum number of issues to retrieve (default: 10)
        """
        token = os.getenv("GITHUB_API_KEY")
        headers = {"Authorization": f"token {token}"} if token else {}
        
        try:
            url = f"https://api.github.com/repos/{repo_full_name}/issues"
            params = {"state": state, "per_page": min(limit, 100)}
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            issues = response.json()
            result = f"{len(issues)} {state} issues for {repo_full_name}:\n\n"
            
            for issue in issues[:limit]:
                # Filter pull requests (they also appear in /issues)
                if 'pull_request' in issue:
                    continue
                    
                number = issue['number']
                title = issue['title']
                user = issue['user']['login']
                created = issue['created_at']
                labels = [label['name'] for label in issue['labels']]
                
                result += f"#{number}: {title}\n"
                result += f"  Created by {user} on {created}\n"
                if labels:
                    result += f"  Labels: {', '.join(labels)}\n"
                result += "\n"
            
            return result
        except Exception as e:
            return f"Error retrieving issues: {str(e)}"


class GitHubPullRequestsTool(BaseTool):
    name: str = "List GitHub Pull Requests"
    description: str = "Lists pull requests of a GitHub repository"
    
    def _run(self, repo_full_name: str, state: str = "open", limit: int = 10) -> str:
        """
        Lists pull requests
        Args:
            repo_full_name: Full name of the repo (e.g., 'owner/repo')
            state: State: 'open', 'closed', 'all' (default: 'open')
            limit: Maximum number of PRs to retrieve (default: 10)
        """
        token = os.getenv("GITHUB_API_KEY")
        headers = {"Authorization": f"token {token}"} if token else {}
        
        try:
            url = f"https://api.github.com/repos/{repo_full_name}/pulls"
            params = {"state": state, "per_page": min(limit, 100)}
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            prs = response.json()
            result = f"{len(prs)} {state} pull requests for {repo_full_name}:\n\n"
            
            for pr in prs[:limit]:
                number = pr['number']
                title = pr['title']
                user = pr['user']['login']
                created = pr['created_at']
                
                result += f"#{number}: {title}\n"
                result += f"  Created by {user} on {created}\n"
                result += f"  {pr['html_url']}\n\n"
            
            return result
        except Exception as e:
            return f"Error retrieving pull requests: {str(e)}"
