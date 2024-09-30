import os
from datetime import date, timedelta
from src.logger import logger  # 引入logger

class ReportGenerator:
    def __init__(self, llm):
        self.llm = llm

    def export_daily_progress(self, repo, updates):
        repo_dir = os.path.join('daily_progress', repo.replace("/", "_"))
        os.makedirs(repo_dir, exist_ok=True)
        
        file_path = os.path.join(repo_dir, f'{date.today()}.md')
        with open(file_path, 'w') as file:
            file.write(f"# Daily Progress for {repo} ({date.today()})\n\n")
            file.write("\n## Issues\n")
            for issue in updates['issues']:
                file.write(f"- {issue['title']} #{issue['number']}\n")
            file.write("\n## Pull Requests\n")
            for pr in updates['pull_requests']:
                file.write(f"- {pr['title']} #{pr['number']}\n")
        return file_path

    def export_progress_by_date_range(self, repo, updates, days):
        repo_dir = os.path.join('daily_progress', repo.replace("/", "_"))
        os.makedirs(repo_dir, exist_ok=True)

        today = date.today()
        since = today - timedelta(days=days)
        
        # Updated filename with date range
        date_str = f"{since}_to_{today}"
        file_path = os.path.join(repo_dir, f'{date_str}.md')
        
        with open(file_path, 'w') as file:
            file.write(f"# Progress for {repo} ({since} to {today})\n\n")
            file.write("\n## Issues Closed in the Last {days} Days\n")
            for issue in updates['issues']:
                file.write(f"- {issue['title']} #{issue['number']}\n")
            file.write("\n## Pull Requests Merged in the Last {days} Days\n")
            for pr in updates['pull_requests']:
                file.write(f"- {pr['title']} #{pr['number']}\n")
        
        logger.info(f"Exported time-range progress to {file_path}")
        return file_path

    def generate_daily_report(self, markdown_file_path):
        with open(markdown_file_path, 'r') as file:
            markdown_content = file.read()

        report = self.llm.summarize_report(markdown_content)

        report_file_path = os.path.splitext(markdown_file_path)[0] + "_report.md"
        with open(report_file_path, 'w+') as report_file:
            report_file.write(report)

        logger.info(f"Generated report saved to {report_file_path}")
        
        return report, report_file_path

    def generate_report_by_date_range(self, markdown_file_path, days):
        with open(markdown_file_path, 'r') as file:
            markdown_content = file.read()

        report = self.llm.summarize_report(markdown_content)

        report_file_path = os.path.splitext(markdown_file_path)[0] + f"_report.md"
        with open(report_file_path, 'w+') as report_file:
            report_file.write(report)

        logger.info(f"Generated report saved to {report_file_path}")
        
        return report, report_file_path

    def export_daily_news(self, updates):
        repo_dir = os.path.join('daily_news')
        os.makedirs(repo_dir, exist_ok=True)

        file_path = os.path.join(repo_dir, f'{date.today()}.md')
        with open(file_path, 'w') as file:
            if updates:
                for idx, story in enumerate(updates, start=1):
                    file.write(f"{idx}. {updates['title']}")
                    file.write(f"   Link: {updates['link']}")
            else:
                file.write("No stories found.")
        return file_path

    def generate_daily_news(self, markdown_file_path):
        with open(markdown_file_path, 'r') as file:
            markdown_content = file.read()

        report = self.llm.summarize_report(markdown_content)

        report_file_path = os.path.splitext(markdown_file_path)[0] + "_report.md"
        with open(report_file_path, 'w+') as report_file:
            report_file.write(report)

        logger.info(f"Generated report saved to {report_file_path}")

        return report, report_file_path