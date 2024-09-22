import threading
import time
from cmd import Cmd
from src.github_client import GitHubClient
from src.subscription_manager import SubscriptionManager
from src.update_fetcher import UpdateFetcher
from src.report_generator import ReportGenerator
from src.daily_progress import DailyProgress
from src.llm_client import LLMClient
from config import GITHUB_TOKEN, OPENAI_API_KEY, LLM_MODEL_TYPE
from datetime import datetime  # 导入 datetime 模块

# 用于全局订阅管理器、报告生成器、每日进展和 LLM 客户端
subscription_manager = SubscriptionManager()
api = GitHubClient(GITHUB_TOKEN)
update_fetcher = UpdateFetcher(api)
report_generator = ReportGenerator()
daily_progress = DailyProgress(GITHUB_TOKEN, subscription_manager.list_subscriptions())
llm_client = LLMClient(OPENAI_API_KEY, model_type=LLM_MODEL_TYPE)


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
        updates = self.api.fetch_updates(subscription_manager.list_subscriptions())
        print(updates)

    def do_daily_progress(self, arg):
        """生成今日进展报告: daily_progress"""
        daily_progress.generate_daily_report()

    def do_daily_summary(self, arg):
        """生成今日进展摘要并汇总: daily_summary"""
        # 生成今日进展报告
        date_str = datetime.now().strftime("%Y-%m-%d")
        markdown_file = f"daily_report_{date_str}.md"

        daily_progress.generate_daily_report()  # 生成报告
        summary = llm_client.summarize_report(markdown_file)  # 调用大模型进行总结

        # 将总结写入文件
        summary_filename = f"summary_report_{date_str}.md"
        with open(summary_filename, "w", encoding="utf-8") as f:
            f.write(summary)

        print(f"已生成总结报告：{summary_filename}")

    def do_exit(self, arg):
        """退出程序: exit"""
        print("退出程序...")
        return True

    def do_help(self, arg):
        """显示帮助信息: help"""
        print("""
            可用命令:
            - add <repository>: 添加新的仓库订阅
            - remove <repository>: 移除已有的仓库订阅
            - list: 列出当前所有订阅的仓库
            - update: 立即获取并显示所有订阅仓库的最新更新
            - daily_progress: 生成今日进展报告
            - daily_summary: 生成今日进展摘要并汇总
            - exit: 退出程序
            """)

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
    sentinel = GitHubSentinel()
    sentinel.do_help("")  # 打印帮助信息
    sentinel.cmdloop()  # 进入命令循环
