class UpdateFetcher:
    def __init__(self, api):
        self.api = api

    def fetch_updates(self, subscriptions):
        updates = {}
        for repo in subscriptions:
            # 初始化一个字典来存储该仓库的信息
            updates[repo] = {}
            updates[repo]['events'] = self.api.get_repo_updates(repo)  # 获取最新事件

            # 获取并存储最新版本信息
            latest_release = self.api.get_latest_release(repo)
            updates[repo]['latest_release'] = latest_release  # 存储最新版本信息

        return updates
