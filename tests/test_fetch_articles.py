"""
fetch_articles.py の単体テスト
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# srcディレクトリをパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from fetch_articles import MeduzaFetcher


class TestMeduzaFetcher(unittest.TestCase):
    """MeduzaFetcherクラスのテスト"""
    
    def setUp(self):
        """テスト前の準備"""
        self.fetcher = MeduzaFetcher()
    
    def test_init(self):
        """初期化テスト"""
        self.assertEqual(self.fetcher.base_url, "https://meduza.io")
        self.assertEqual(self.fetcher.rss_url, "https://meduza.io/rss/all")
    
    @patch('fetch_articles.feedparser.parse')
    def test_fetch_rss_feed_success(self, mock_parse):
        """RSS取得成功テスト"""
        # モックデータの準備
        mock_entry = MagicMock()
        mock_entry.title = "テストニュース"
        mock_entry.link = "https://meduza.io/test"
        mock_entry.published = "2023-01-01"
        mock_entry.summary = "テスト要約"
        mock_entry.get.return_value = []
        
        mock_feed = MagicMock()
        mock_feed.entries = [mock_entry]
        mock_parse.return_value = mock_feed
        
        # テスト実行
        result = self.fetcher.fetch_rss_feed()
        
        # 検証
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['title'], "テストニュース")
        self.assertEqual(result[0]['link'], "https://meduza.io/test")
    
    @patch('fetch_articles.feedparser.parse')
    def test_fetch_rss_feed_error(self, mock_parse):
        """RSS取得エラーテスト"""
        # 例外を発生させる
        mock_parse.side_effect = Exception("Network Error")
        
        # テスト実行
        result = self.fetcher.fetch_rss_feed()
        
        # 検証
        self.assertIsNone(result)
    
    def test_fetch_article_content_not_implemented(self):
        """記事コンテンツ取得（未実装）テスト"""
        result = self.fetcher.fetch_article_content("https://meduza.io/test")
        self.assertIsNone(result)


class TestIntegration(unittest.TestCase):
    """統合テスト"""
    
    def test_fetcher_creation(self):
        """フェッチャー作成テスト"""
        fetcher = MeduzaFetcher()
        self.assertIsInstance(fetcher, MeduzaFetcher)


if __name__ == '__main__':
    # テスト実行
    unittest.main(verbosity=2)
