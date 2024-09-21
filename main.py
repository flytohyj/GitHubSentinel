import threading
import time
from cmd import Cmd
from src.github_api import GitHubAPI
from src.subscription_manager import SubscriptionManager
from src.update_fetcher import UpdateFetcher
from src.report_generator import ReportGenerator
from config import GITHUB_TOKEN

# 用于全局订阅管理器和报告生成器
subscription_manager = SubscriptionManager()
api = GitHubAPI(GITHUB_TOKEN)
update_fetcher = UpdateFetcher(api)
report_generator = ReportGenerator()


class GitHubSentinel(Cmd):
    intro = '欢迎使用 GitHub Sentinel! 输入 help 获取帮助.'
    prompt = '(GitHubSentinel) '

    def do_add(self, repo):
        """添加新的仓库订阅: add <repository>"""
        if repo:
            subscription_manager.add_subscription(repo)
            print(f"已添加订阅: {repo}")
        else:
            print("请输入要添加的仓库名。")

    def do_remove(self, repo):
        """移除已有的仓库订阅: remove <repository>"""
        if repo:
            subscription_manager.remove_subscription(repo)
            print(f"已移除订阅: {repo}")
        else:
            print("请输入要移除的仓库名。")

    def do_list(self, arg):
        """列出当前所有订阅的仓库: list"""
        subscriptions = subscription_manager.list_subscriptions()
        if subscriptions:
            print("当前订阅的仓库:")
            for sub in subscriptions:
                print(f"- {sub}")
        else:
            print("没有订阅任何仓库。")

    def do_update(self, arg):
        """立即获取并显示所有订阅仓库的最新更新: update"""
        updates = update_fetcher.fetch_updates(subscription_manager.list_subscriptions())
        report = report_generator.generate_report(updates)
        print(report)

    def do_exit(self, arg):
        """退出程序: exit"""
        print("退出程序...")
        return True

    def fetch_and_print_updates(self):
        """后台线程定期检查更新"""
        while True:
            updates = update_fetcher.fetch_updates(subscription_manager.list_subscriptions())
            report = report_generator.generate_report(updates)
            print(report)
            time.sleep(60)  # 每60秒检查一次更新


if __name__ == '__main__':
    # 启动后台线程定期检查更新
    threading.Thread(target=GitHubSentinel().fetch_and_print_updates, daemon=True).start()

    # 启动命令行交互
    GitHubSentinel().cmdloop()
