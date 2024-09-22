import requests
import datetime

class GitHubClient:
    def __init__(self, token):
        self.token = token
        self.headers = {'Authorization': f'token {self.token}'}

    def fetch_updates(self, repo):
        """获取特定 repo 的更新（commits, issues, pull requests）"""
        updates = {
            'commits': self.fetch_commits(repo),
            'issues': self.fetch_issues(repo),
            'pull_requests': self.fetch_pull_requests(repo)
        }
        return updates

    def fetch_commits(self, repo):
        """获取特定 repo 的提交记录"""
        url = f'https://api.github.com/repos/{repo}/commits'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def fetch_issues(self, repo):
        """获取特定 repo 的问题列表"""
        url = f'https://api.github.com/repos/{repo}/issues'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def fetch_pull_requests(self, repo):
        """获取特定 repo 的拉取请求列表"""
        url = f'https://api.github.com/repos/{repo}/pulls'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_latest_release(self, repo):
        """获取特定 repo 的最新版本信息"""
        url = f'https://api.github.com/repos/{repo}/releases/latest'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
