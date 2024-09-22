import requests
from datetime import datetime, date, timedelta
import os
from src.logger import logger


class GitHubClient:
    def __init__(self, token):
        self.token = token
        self.headers = {'Authorization': f'token {self.token}'}

    def fetch_updates(self, repo, since_format=None, until_format=None):
        updates = {
            'commits': self.fetch_commits(repo, since_format, until_format),
            'issues': self.fetch_issues(repo, since_format, until_format),
            'pull_requests': self.fetch_pull_requests(repo, since_format, until_format)
        }
        return updates

    def fetch_commits(self, repo, since=None, until=None):
        url = f'https://api.github.com/repos/{repo}/commits'
        params = {}
        if since:
            params['since'] = since
        if until:
            params['until'] = until

        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        logger.info(f"请求接口{url}========返回内容= {response.json()}")
        return response.json()

    def fetch_issues(self, repo, since=None, until=None):
        url = f'https://api.github.com/repos/{repo}/issues'
        params = {
            'state': 'closed',
            'since': since,
            'until': until
        }
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        logger.info(f"请求接口{url}========返回内容= {response.json()}")
        return response.json()

    def fetch_pull_requests(self, repo, since=None, until=None):
        url = f'https://api.github.com/repos/{repo}/pulls'
        params = {
            'state': 'closed',
            'since': since,
            'until': until
        }
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        logger.info(f"请求接口{url}========返回内容= {response.json()}")
        return response.json()

    def export_daily_progress(self, repo):
        today = datetime.now().date().isoformat()
        updates = self.fetch_updates(repo, today)

        repo_dir = os.path.join('daily_progress', repo.replace("/", "_"))
        os.makedirs(repo_dir, exist_ok=True)

        file_path = os.path.join(repo_dir, f'{today}.md')
        with open(file_path, 'w') as file:
            file.write(f"# Daily Progress for {repo} ({today})\n\n")
            file.write("\n## Issues Closed Today\n")
            for issue in updates['issues']:
                file.write(f"- {issue['title']} #{issue['number']}\n")
            file.write("\n## Pull Requests Merged Today\n")
            for pr in updates['pull_requests']:
                file.write(f"- {pr['title']} #{pr['number']}\n")

        logger.info(f"Exported daily progress to {file_path}")
        return file_path

    def export_progress_by_date_range(self, repo,  since=None, until=None):
        if not until:
            until = date.today()
        updates = self.fetch_updates(repo, since, until)
        repo_dir = os.path.join('daily_progress', repo.replace("/", "_"))
        os.makedirs(repo_dir, exist_ok=True)

        # Updated filename with date range
        date_str = f"{since}_to_{until}"
        file_path = os.path.join(repo_dir, f'{date_str}.md')

        with open(file_path, 'w') as file:
            file.write(f"# Progress for {repo} ({since} to {until})\n\n")
            file.write("\n## Issues Closed in the Last {days} Days\n")
            for issue in updates['issues']:
                file.write(f"- {issue['title']} #{issue['number']}\n")
            file.write("\n## Pull Requests Merged in the Last {days} Days\n")
            for pr in updates['pull_requests']:
                file.write(f"- {pr['title']} #{pr['number']}\n")

        logger.info(f"Exported time-range progress to {file_path}")
        return file_path