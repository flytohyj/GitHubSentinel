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

    def export_daily_progress(self, repo):
        """导出指定 repo 的每日进度报告到 Markdown 文件"""
        date_str = datetime.datetime.now().strftime('%Y-%m-%d')
        issues = self.fetch_issues(repo)
        pull_requests = self.fetch_pull_requests(repo)
        filename = f'daily_progress/{repo.replace("/", "_")}_{date_str}.md'

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# {repo} Daily Progress - {date_str}\n\n")
            f.write("## Issues\n")
            if issues:
                for issue in issues:
                    f.write(f"- [{issue['title']}](https://github.com/{repo}/issues/{issue['number']}) #{issue['number']}\n")
            else:
                f.write("没有开放的问题。\n")

            f.write("\n## Pull Requests\n")
            if pull_requests:
                for pr in pull_requests:
                    f.write(f"- [{pr['title']}](https://github.com/{repo}/pull/{pr['number']}) #{pr['number']}\n")
            else:
                f.write("没有开放的拉取请求。\n")

        print(f"Exported daily progress to {filename}")
        return filename
