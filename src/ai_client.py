import requests
from bs4 import BeautifulSoup


class AiClient:
    def __init__(self):
        self.url = 'https://www.aihub.cn/news/'
        self.headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
                    }

    def fetch_ai_news_top_stories(self):
        response = requests.get(self.url, headers=self.headers)
        response.raise_for_status()  # 检查请求是否成功

        soup = BeautifulSoup(response.text, 'html.parser')
        # 查找包含新闻的所有 <tr> 标签
        news_items = soup.find_all('div', class_='post-info')

        top_news = []
        for item in news_items:
            # 提取标题和链接
            title = item.find('a').text.strip()  # 假设标题在 <a> 标签中
            link = item.find('a')['href']  # 获取链接
            if title:
                top_news.append({'title': title, 'link': link})
        return top_news