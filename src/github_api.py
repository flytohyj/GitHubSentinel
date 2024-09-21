from github import Github

class GitHubAPI:
    def __init__(self, token):
        self.token = token
        self.github = Github(token)

    def get_repo_updates(self, repo):
        repository = self.github.get_repo(repo)
        events = repository.get_events()
        return [event.raw_data for event in events]

    def get_latest_release(self, repo):
        repository = self.github.get_repo(repo)
        releases = repository.get_releases()
        return releases[0] if releases.totalCount > 0 else None
