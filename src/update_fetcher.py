class UpdateFetcher:
    def __init__(self, api):
        self.api = api

    def fetch_updates(self, subscriptions,since_format=None, until_format=None):
        updates = {}
        for repo in subscriptions:
            # 初始化一个字典来存储该仓库的信息
            updates[repo] = {}
            updates[repo] = self.api.fetch_updates(repo,since_format,until_format)  # 获取最新事件

        return updates

    def fetch_updates(self, subscriptions,since_format=None, until_format=None):
        updates = {}
        for repo in subscriptions:
            # 初始化一个字典来存储该仓库的信息
            updates[repo] = {}
            updates[repo] = self.api.fetch_updates(repo,since_format,until_format)  # 获取最新事件

        return updates
