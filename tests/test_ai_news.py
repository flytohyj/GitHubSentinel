import requests
from bs4 import BeautifulSoup

# 设置请求头，伪装成浏览器
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
}

# 目标网址
url = 'https://www.aihub.cn/news/'

# 发起请求并获取页面内容
response = requests.get(url, headers=headers)

# 检查响应状态
if response.status_code == 200:
    # 解析网页内容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 找到所有新闻项，这里假设每个新闻项在一个特定的类名下
    news_items = soup.find_all('div', class_='post-info')  # 请根据实际网页结构调整类名

    for item in news_items:
        # 提取标题和链接
        title = item.find('a').text.strip()  # 假设标题在 <a> 标签中
        link = item.find('a')['href']  # 获取链接

        # 输出结果
        print(f'标题: {title}')
        print(f'链接: {link}')
        print('---')
else:
    print(f'无法访问页面，状态码: {response.status_code}')
