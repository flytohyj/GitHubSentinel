from github import Github
from datetime import datetime
import os


class DailyProgress:
    def __init__(self, token, subscriptions):
        self.github = Github(token)
        self.subscriptions = subscriptions

    def generate_daily_report(self):
        date_str = datetime.now().strftime("%Y-%m-%d")
        report_lines = []

        for repo in self.subscriptions:
            repository = self.github.get_repo(repo)
            report_lines.append(f"# {repo} - {date_str}\n")

            # 获取 issues 列表
            report_lines.append("## Issues\n")
            issues = repository.get_issues(state='open')
            if issues.totalCount == 0:
                report_lines.append("没有开放的 issues。\n")
            else:
                for issue in issues:
                    report_lines.append(f"- [{issue.title}]({issue.html_url}) - 提交者: {issue.user.login}\n")

            # 获取 pull requests 列表
            report_lines.append("\n## Pull Requests\n")
            pulls = repository.get_pulls(state='open')
            if pulls.totalCount == 0:
                report_lines.append("没有开放的 pull requests。\n")
            else:
                for pr in pulls:
                    report_lines.append(f"- [{pr.title}]({pr.html_url}) - 提交者: {pr.user.login}\n")

            report_lines.append("\n---\n")

        # 生成 markdown 文件
        report_filename = f"daily_report_{date_str}.md"
        with open(report_filename, "w", encoding="utf-8") as f:
            f.write("\n".join(report_lines))

        print(f"已生成报告：{report_filename}")
