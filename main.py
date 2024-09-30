import gradio as gr
import requests
from bs4 import BeautifulSoup
from src.github_client import GitHubClient
from src.hacker_client import HackerClient
from src.subscription_manager import SubscriptionManager
from src.llm_client import LLMClient
from config import GITHUB_TOKEN, OPENAI_API_KEY, LLM_MODEL_TYPE
from datetime import datetime
from src.logger import logger  # 引入logger
from src.report_generator import ReportGenerator
# 配置日志
logger.info("Starting the GitHub Sentinel application...")

# 用于全局订阅管理器、报告生成器、每日进展和 LLM 客户端
subscription_manager = SubscriptionManager()
gitHub_client = GitHubClient(GITHUB_TOKEN)
llm_client = LLMClient(OPENAI_API_KEY, model_type=LLM_MODEL_TYPE)
report_generator = ReportGenerator(llm_client)
hacker_client =HackerClient()


def add_subscription(repo):
    """添加新的仓库订阅"""
    if not repo or repo.strip() == "":
        return "请输入有效的仓库名（例如：owner/repo）。"

    result_message = subscription_manager.add_subscription(repo)
    logger.info(f"Added subscription for repo: {repo}")
    return result_message


def remove_subscription(repo):
    """移除已有的仓库订阅"""
    result_message = subscription_manager.remove_subscription(repo)
    logger.info(f"Removed subscription for repo: {repo}")
    return result_message


def list_subscriptions():
    """列出当前所有订阅的仓库"""
    subscriptions = subscription_manager.list_subscriptions()
    logger.info("Listing all subscriptions.")
    if subscriptions:
        return "当前订阅的仓库:\n" + "\n".join([f"- {sub}" for sub in subscriptions])
    else:
        return "没有订阅任何仓库。"


def update_subscriptions(since=None, until=None):
    """立即获取并显示所有订阅仓库的最新更新"""
    subscriptions = subscription_manager.list_subscriptions()
    if not subscriptions:
        logger.warning("Attempted to update subscriptions but no repositories are subscribed.")
        return "没有订阅任何仓库，无法进行更新。请先添加仓库订阅。"

    # 将日期转换为 ISO 8601 格式
    since_format = None
    until_format = None
    if since:
        if isinstance(since, float):
            # Convert float timestamp to datetime
            since_datetime = datetime.fromtimestamp(since)
        else:
            # Assume it's a string in the format "YYYY-MM-DD HH:MM:SS"
            since_datetime = datetime.strptime(since, "%Y-%m-%d %H:%M:%S")
        since_format = since_datetime.isoformat()
    if until:
        if isinstance(until, float):
            # Convert float timestamp to datetime
            until_datetime = datetime.fromtimestamp(until)
        else:
            # Assume it's a string in the format "YYYY-MM-DD HH:MM:SS"
            until_datetime = datetime.strptime(until, "%Y-%m-%d %H:%M:%S")
        until_format = until_datetime.isoformat()  # 转换成 ISO 8601 格式

    updates = {}
    for repo in subscriptions:
        # 初始化一个字典来存储该仓库的信息
        updates[repo] = {}
        updates[repo] = gitHub_client.fetch_updates(repo, since_format, until_format)  # 获取最新事件

    logger.info("Updated subscriptions with new data.")
    return updates


def generate_daily_progress():
    """生成今日进展报告"""
    subscriptions = subscription_manager.list_subscriptions()
    if not subscriptions:
        logger.warning("No subscriptions found when generating daily report.")
        return "没有订阅任何仓库，无法进行生成。请先添加仓库订阅。"
    since_format = datetime.now().date().isoformat()
    updates = {}
    for repo in subscriptions:
        # 初始化一个字典来存储该仓库的信息
        updates[repo] = {}
        updates[repo] = gitHub_client.export_daily_progress(repo)  # 获取最新事件
    logger.info(f"Daily progress report generated: {updates}")
    return updates


def generate_daily_summary():
    """生成今日进展摘要并汇总"""
    subscriptions = subscription_manager.list_subscriptions()
    if not subscriptions:
        logger.warning("No subscriptions found when generating daily summary.")
        return "没有订阅任何仓库，无法进行生成。请先添加仓库订阅。"

    since_format = datetime.now().date().isoformat()
    reports={}
    for repo in subscriptions:
        # 初始化一个字典来存储该仓库的信息
        updates = gitHub_client.fetch_updates(repo, since_format)
        file_path = report_generator.export_daily_progress(repo, updates)
        report, markdown_file = report_generator.generate_daily_report(file_path)  # 生成报告
        reports[repo] = report
    logger.info(f"Daily summary report generated: {reports}")
    return f"已生成总结报告：{reports}"


def fetch_hackernews_summary():
    news = hacker_client.fetch_hackernews_top_stories()
    print(news)
    file_path = report_generator.export_daily_news(news)
    report, markdown_file = report_generator.generate_daily_report(file_path)  # 生成报告
    logger.info(f"Hacker news summary report generated: {report}")
    return f"已生成Hacker总结报告：{report}"


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

    with gr.Row():
        since_input = gr.DateTime(label="开始日期 (Since)")  # 使用 gr.DateTime
        until_input = gr.DateTime(label="结束日期 (Until)")  # 使用 gr.DateTime

    update_button = gr.Button("更新订阅")
    update_button.click(update_subscriptions, inputs=[since_input, until_input], outputs=output_text)

    daily_report_button = gr.Button("生成今日进展报告")
    daily_report_button.click(generate_daily_progress, outputs=output_text)

    daily_summary_button = gr.Button("生成今日进展摘要")
    daily_summary_button.click(generate_daily_summary, outputs=output_text)

    fetch_hackernews_button = gr.Button("获取Hack 新闻")
    fetch_hackernews_button.click(fetch_hackernews_summary, outputs=output_text)

# 启动 Gradio 应用
if __name__ == '__main__':
    demo.launch()
