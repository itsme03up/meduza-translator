"""
RSS記事取得ロジック
Meduzaサイトからニュース記事を取得する
"""

import requests
import feedparser
from typing import List, Dict, Optional
import logging

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MeduzaFetcher:
    """Meduzaからニュース記事を取得するクラス"""
    
    def __init__(self):
        self.base_url = "https://meduza.io"
        self.rss_url = "https://meduza.io/rss/all"
    
    def fetch_rss_feed(self) -> Optional[List[Dict]]:
        """
        RSSフィードから記事一覧を取得
        
        Returns:
            List[Dict]: 記事データのリスト
        """
        try:
            logger.info(f"RSSフィードを取得中: {self.rss_url}")
            feed = feedparser.parse(self.rss_url)
            
            articles = []
            for entry in feed.entries:
                article = {
                    'title': entry.title,
                    'link': entry.link,
                    'published': entry.get('published', ''),
                    'summary': entry.get('summary', ''),
                    'content': entry.get('content', [{}])[0].get('value', '') if entry.get('content') else ''
                }
                articles.append(article)
            
            logger.info(f"取得した記事数: {len(articles)}")
            return articles
            
        except Exception as e:
            logger.error(f"RSS取得エラー: {e}")
            return None
    
    def fetch_article_content(self, url: str) -> Optional[str]:
        """
        指定URLから記事の詳細コンテンツを取得
        
        Args:
            url (str): 記事のURL
            
        Returns:
            Optional[str]: 記事コンテンツ
        """
        try:
            logger.info(f"記事コンテンツを取得中: {url}")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Meduzaサイトの記事本文を抽出
            # 一般的な記事セレクタを試す
            content_selectors = [
                'div.GeneralMaterial-article',
                'div.RichText',
                'div.SimpleBlock-article',
                'article',
                '.article-content',
                '.post-content'
            ]
            
            for selector in content_selectors:
                content_div = soup.select_one(selector)
                if content_div:
                    # テキストのみ抽出、改行を保持
                    paragraphs = content_div.find_all(['p', 'div', 'span'])
                    content = '\n'.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
                    if content and len(content) > 100:  # 最小限の長さチェック
                        return content
            
            # フォールバック: すべてのpタグを取得
            paragraphs = soup.find_all('p')
            content = '\n'.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
            
            return content if content else "記事本文の抽出に失敗しました"
            
        except Exception as e:
            logger.error(f"記事取得エラー: {e}")
            return f"記事取得エラー: {str(e)}"


def fetch_meduza_articles(limit: int = 5) -> List[Dict]:
    """
    Meduzaから記事を取得する便利関数
    
    Args:
        limit: 取得する記事数
        
    Returns:
        List[Dict]: 記事データのリスト
    """
    fetcher = MeduzaFetcher()
    articles = fetcher.fetch_rss_feed()
    
    if not articles:
        return []
    
    # limit件に制限
    limited_articles = articles[:limit]
    
    # 各記事の本文も取得
    for article in limited_articles:
        content = fetcher.fetch_article_content(article['link'])
        article['content'] = content or "本文取得失敗"
    
    return limited_articles


def main():
    """テスト実行"""
    fetcher = MeduzaFetcher()
    articles = fetcher.fetch_rss_feed()
    
    if articles:
        print(f"取得した記事数: {len(articles)}")
        for i, article in enumerate(articles[:3]):  # 最初の3記事を表示
            print(f"\n{i+1}. {article['title']}")
            print(f"   URL: {article['link']}")
            print(f"   公開日: {article['published']}")


if __name__ == "__main__":
    main()
