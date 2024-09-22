class ReportGenerator:
    def generate_report(self, updates):
        report = ""
        for repo, data in updates.items():
            report += f"### Repository: {repo}\n\n"

            if not data:  # 检查数据是否为空
                report += "#### No data found for this repository.\n"
                continue

            # Ensure 'events' and 'latest_release' are present
            events = data.get('events', [])
            latest_release = data.get('latest_release', None)

            if events:
                report += "#### Latest Events:\n"
                for event in events:
                    report += f"- {event['type']} at {event['created_at']}\n"
            else:
                report += "#### No events found.\n"

            if latest_release:
                report += f"#### Latest Release: {latest_release['tag_name']} - {latest_release['published_at']}\n"
                report += f"#### Release URL: [Link](https://github.com/{repo}/releases/tag/{latest_release['tag_name']})\n\n"
            else:
                report += "#### No releases found.\n"

        return report

    def export_daily_progress(self, subscriptions, filename):
        if not subscriptions:  # 检查 subscriptions 是否存在
            print("没有可用的订阅，无法导出日报。")
            return  # 提前结束，避免后续错误

        updates = {}
        for repo in subscriptions:
            try:
                updates[repo] = {
                    'events': self.fetch_events(repo),  # 自定义函数来获取事件
                    'latest_release': self.get_latest_release(repo)  # 假设有一个函数来获取最新发布
                }
            except Exception as e:
                print(f"Error fetching updates for {repo}: {e}")
                updates[repo] = None  # 确保即使出错也不会让整个循环崩溃

        # 生成报告
        report = self.generate_report(updates)

        # 导出为 Markdown 文件
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"Exported daily progress to {filename}")

    def fetch_events(self, repo):
        # 这个函数需要实现，返回 repo 的事件数据
        pass

    def get_latest_release(self, repo):
        # 这个函数需要实现，返回 repo 的最新版本信息
        pass
