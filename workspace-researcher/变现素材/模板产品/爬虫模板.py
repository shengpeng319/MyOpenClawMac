"""
通用爬虫模板 - 可直接使用
价格: 29.9元
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

class SimpleCrawler:
    def __init__(self, url):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def crawl(self):
        response = requests.get(self.url, headers=self.headers)
        return BeautifulSoup(response.text, 'html.parser')
    
    def save_to_csv(self, data, filename='data.csv'):
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"已保存到 {filename}")

# 使用示例
if __name__ == "__main__":
    # 替换为目标URL
    url = "https://example.com"
    crawler = SimpleCrawler(url)
    soup = crawler.crawl()
    print(soup.title)
