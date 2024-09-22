# tests/test_daily_progress.py
import os
import unittest
from src.daily_progress import DailyProgress

class TestDailyProgress(unittest.TestCase):
    def setUp(self):
        self.token = ""
        self.subscriptions = ["langchain-ai/langchain"]
        self.daily_progress = DailyProgress(self.token, self.subscriptions)

    def test_generate_daily_report(self):
        report_file = self.daily_progress.generate_daily_report()
        self.assertTrue(os.path.exists(report_file))

if __name__ == '__main__':
    unittest.main()
