import threading
import time
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


def fetch_and_print_updates():
    while True:
        # 获取所有订阅的更新
        updates = update_fetcher.fetch_updates(subscription_manager.list_subscriptions())
        report = report_generator.generate_report(updates)
        print(report)
        time.sleep(60)  # 每60秒检查一次更新


def command_input():
    while True:
        cmd = input("\n请输入命令 (add/remove/list/update/exit): ").strip().lower()
        if cmd.startswith("add "):
            repo = cmd[4:].strip()
            subscription_manager.add_subscription(repo)
            print(f"已添加订阅: {repo}")
        elif cmd.startswith("remove "):
            repo = cmd[7:].strip()
            subscription_manager.remove_subscription(repo)
            print(f"已移除订阅: {repo}")
        elif cmd == "list":
            subscriptions = subscription_manager.list_subscriptions()
            print("当前订阅的仓库:")
            for sub in subscriptions:
                print(f"- {sub}")
        elif cmd == "update":
            updates = update_fetcher.fetch_updates(subscription_manager.list_subscriptions())
            report = report_generator.generate_report(updates)
            print(report)
        elif cmd == "exit":
            print("退出程序...")
            break
        else:
            print("无效命令，请重试。")


if __name__ == '__main__':
    # 启动后台线程定期检查更新
    threading.Thread(target=fetch_and_print_updates, daemon=True).start()

    # 开始命令输入
    command_input()
