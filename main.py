from src.github_api import GitHubAPI
from src.subscription_manager import SubscriptionManager
from src.update_fetcher import UpdateFetcher
from src.report_generator import ReportGenerator
from config import GITHUB_TOKEN, SUBSCRIPTIONS

def main():
    api = GitHubAPI(GITHUB_TOKEN)
    subscription_manager = SubscriptionManager()
    
    for sub in SUBSCRIPTIONS:
        subscription_manager.add_subscription(sub)
    
    update_fetcher = UpdateFetcher(api)
    updates = update_fetcher.fetch_updates(subscription_manager.list_subscriptions())
    
    report_generator = ReportGenerator()
    report = report_generator.generate_report(updates)
    
    print(report)

if __name__ == '__main__':
    main()
