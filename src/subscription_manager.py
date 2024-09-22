class SubscriptionManager:
    def __init__(self):
        self.subscriptions = []

    def add_subscription(self, repo):
        """添加新的仓库订阅"""
        if repo in self.subscriptions:
            return f"仓库 {repo} 已经存在于订阅列表中。"
        else:
            self.subscriptions.append(repo)
            return f"已添加订阅: {repo}"

    def remove_subscription(self, repo):
        """移除已有的仓库订阅"""
        if repo not in self.subscriptions:
            return f"仓库 {repo} 不在订阅列表中，无法移除。"
        else:
            self.subscriptions.remove(repo)
            return f"已移除订阅: {repo}"

    def list_subscriptions(self):
        """列出当前所有订阅的仓库"""
        return self.subscriptions

