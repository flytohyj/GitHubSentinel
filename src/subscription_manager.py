class SubscriptionManager:
    def __init__(self):
        self.subscriptions = []

    def add_subscription(self, repo):
        self.subscriptions.append(repo)

    def remove_subscription(self, repo):
        self.subscriptions.remove(repo)

    def list_subscriptions(self):
        return self.subscriptions
