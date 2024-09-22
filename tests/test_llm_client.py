import unittest
from src.llm_client import LLMClient  # 假设 llm_client.py 在当前目录下


class TestLLMClient(unittest.TestCase):
    def setUp(self):
        # 设置初始条件
        self.model_type = 'tongyi'
        self.api_key = 'sk-82100ed30afe4ae2af3f4f25b80cc204	'
        self.client = LLMClient(self.api_key, self.model_type)


    def test_summarize_with_tongyiqianwen(self):
        # 模拟通义千问 API 的响应
        summary = self.client.summarize_report("daily_report_2024-09-22.md")
        print(summary)


    def tearDown(self):
        # 清理操作，如果需要的话
        pass


if __name__ == '__main__':
    unittest.main()
