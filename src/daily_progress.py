from src.report_generator import ReportGenerator
from datetime import datetime



class DailyProgress:
    def __init__(self, token, subscriptions):
        self.token = token
        self.subscriptions = subscriptions
        self.report_generator = ReportGenerator()  # 初始化 ReportGenerator 实例

    def generate_daily_report(self):
        date_str = datetime.now().strftime('%Y-%m-%d')
        filename = f'daily_progress_report_{date_str}.md'
        # 调用 export_daily_progress 方法来生成报告
        if not self.subscriptions:  # 检查是否有订阅
            return "没有订阅仓库，无法生成日报。"

        self.report_generator.export_daily_progress(self.subscriptions, filename)
        return filename
