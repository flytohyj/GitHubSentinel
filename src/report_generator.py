class ReportGenerator:
    def generate_report(self, updates):
        report_lines = []
        for repo, data in updates.items():
            report_lines.append(f"**Repository:** {repo}\n")
            report_lines.append("**Latest Events:**\n")
            for event in data['events']:
                report_lines.append(f"- {event['type']} at {event['created_at']}\n")

            latest_release = data.get('latest_release')
            if latest_release:
                report_lines.append(f"**Latest Release:** {latest_release.title} - {latest_release.published_at}\n")
                report_lines.append(f"**Release URL:** [Link]({latest_release.html_url})\n")
            else:
                report_lines.append("**Latest Release:** No releases found.\n")

        return "\n".join(report_lines)
