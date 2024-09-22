import threading
import time
import gradio as gr
from src.github_client import GitHubClient
from src.subscription_manager import SubscriptionManager
from src.update_fetcher import UpdateFetcher
from src.report_generator import ReportGenerator
from src.daily_progress import DailyProgress
from src.llm_client import LLMClient
from config import GITHUB_TOKEN, OPENAI_API_KEY, LLM_MODEL_TYPE
from datetime import datetime

# 用于全局订阅管理器、报告生成器、每日进展和 LLM 客户端
subscription_manager = SubscriptionManager()
api = GitHubClient(GITHUB_TOKEN)
update_fetcher = UpdateFetcher(api)
report_generator = ReportGenerator()
daily_progress = DailyProgress(GITHUB_TOKEN, subscription_manager.list_subscriptions())
llm_client = LLMClient(OPENAI_API_KEY, model_type=LLM_MODEL_TYPE)


def add_subscription(repo):
    """添加新的仓库订阅"""
    result_message = subscription_manager.add_subscription(repo)
    return result_message


def remove_subscription(repo):
    """移除已有的仓库订阅"""
    result_message = subscription_manager.remove_subscription(repo)
    return result_message


def list_subscriptions():
    """列出当前所有订阅的仓库"""
    subscriptions = subscription_manager.list_subscriptions()
    if subscriptions:
        return "当前订阅的仓库:\n" + "\n".join([f"- {sub}" for sub in subscriptions])
    else:
        return "没有订阅任何仓库。"


def update_subscriptions():
    """立即获取并显示所有订阅仓库的最新更新"""
    subscriptions = subscription_manager.list_subscriptions()
    if not subscriptions:
        return "没有订阅任何仓库，无法进行更新。请先添加仓库订阅。"

    updates = update_fetcher.fetch_updates(subscriptions)
    report = report_generator.generate_report(updates)
    return report


def generate_daily_report():
    """生成今日进展报告"""
    subscriptions = subscription_manager.list_subscriptions()
    if not subscriptions:
        return "没有订阅任何仓库，无法进行生成。请先添加仓库订阅。"
    filename = daily_progress.generate_daily_report()  # 调用 DailyProgress 的方法
    return f"今日进展报告已生成：{filename}"


def generate_daily_summary():
    """生成今日进展摘要并汇总"""
    subscriptions = subscription_manager.list_subscriptions()
    if not subscriptions:
        return "没有订阅任何仓库，无法进行生成。请先添加仓库订阅。"
    date_str = datetime.now().strftime("%Y-%m-%d")

    markdown_file = daily_progress.generate_daily_report()  # 生成报告
    summary = llm_client.summarize_report(markdown_file)  # 调用大模型进行总结

    summary_filename = f"summary_report_{date_str}.md"
    with open(summary_filename, "w", encoding="utf-8") as f:
        f.write(summary)

    return f"已生成总结报告：{summary_filename}"


# Gradio界面设计
with gr.Blocks() as demo:
    gr.Markdown("# GitHub Sentinel")

    repo_input = gr.Textbox(label="仓库名 (例如: owner/repo)", placeholder="输入要添加或移除的仓库名...")

    with gr.Row():
        add_button = gr.Button("添加订阅")
        remove_button = gr.Button("移除订阅")

    output_text = gr.Textbox(label="输出", interactive=False)

    add_button.click(add_subscription, inputs=repo_input, outputs=output_text)
    remove_button.click(remove_subscription, inputs=repo_input, outputs=output_text)

    list_button = gr.Button("列出订阅")
    list_button.click(list_subscriptions, outputs=output_text)

    update_button = gr.Button("更新订阅")
    update_button.click(update_subscriptions, outputs=output_text)

    daily_report_button = gr.Button("生成今日进展报告")
    daily_report_button.click(generate_daily_report, outputs=output_text)

    daily_summary_button = gr.Button("生成今日进展摘要")
    daily_summary_button.click(generate_daily_summary, outputs=output_text)

# 启动 Gradio 应用
if __name__ == '__main__':
    demo.launch()
