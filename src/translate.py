"""
翻訳処理（googletrans使用）
ロシア語記事を日本語に翻訳する
"""

from googletrans import Translator
from typing import Optional, Dict
import logging
import time

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MeduzaTranslator:
    """Google Translateを使用した翻訳クラス"""
    
    def __init__(self):
        self.translator = Translator()
        self.source_lang = 'ru'  # ロシア語
        self.target_lang = 'ja'  # 日本語
    
    def translate_text(self, text: str, delay: float = 1.0) -> Optional[str]:
        """
        テキストを翻訳
        
        Args:
            text (str): 翻訳対象のテキスト
            delay (float): API制限対策の遅延時間（秒）
            
        Returns:
            Optional[str]: 翻訳済みテキスト
        """
        if not text or not text.strip():
            return ""
        
        try:
            logger.info(f"翻訳中... (文字数: {len(text)})")
            
            # レート制限対策
            time.sleep(delay)
            
            # 翻訳実行
            result = self.translator.translate(
                text, 
                src=self.source_lang, 
                dest=self.target_lang
            )
            
            translated_text = result.text
            logger.info(f"翻訳完了 (文字数: {len(translated_text)})")
            
            return translated_text
            
        except Exception as e:
            logger.error(f"翻訳エラー: {e}")
            return None
    
    def translate_article(self, article: Dict) -> Optional[Dict]:
        """
        記事全体を翻訳
        
        Args:
            article (Dict): 記事データ
            
        Returns:
            Optional[Dict]: 翻訳済み記事データ
        """
        try:
            translated_article = article.copy()
            
            # タイトルを翻訳
            if article.get('title'):
                translated_title = self.translate_text(article['title'])
                if translated_title:
                    translated_article['title_ja'] = translated_title
            
            # 要約を翻訳
            if article.get('summary'):
                translated_summary = self.translate_text(article['summary'])
                if translated_summary:
                    translated_article['summary_ja'] = translated_summary
            
            # コンテンツを翻訳（長い場合は分割）
            if article.get('content'):
                translated_content = self.translate_long_text(article['content'])
                if translated_content:
                    translated_article['content_ja'] = translated_content
            
            logger.info("記事翻訳完了")
            return translated_article
            
        except Exception as e:
            logger.error(f"記事翻訳エラー: {e}")
            return None
    
    def translate_long_text(self, text: str, chunk_size: int = 4000) -> Optional[str]:
        """
        長いテキストを分割して翻訳
        
        Args:
            text (str): 翻訳対象のテキスト
            chunk_size (int): 分割サイズ
            
        Returns:
            Optional[str]: 翻訳済みテキスト
        """
        if len(text) <= chunk_size:
            return self.translate_text(text)
        
        try:
            # テキストを分割
            chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
            translated_chunks = []
            
            for i, chunk in enumerate(chunks):
                logger.info(f"チャンク {i+1}/{len(chunks)} を翻訳中...")
                translated_chunk = self.translate_text(chunk, delay=2.0)
                
                if translated_chunk:
                    translated_chunks.append(translated_chunk)
                else:
                    logger.warning(f"チャンク {i+1} の翻訳に失敗")
                    translated_chunks.append(chunk)  # 原文をそのまま使用
            
            return ' '.join(translated_chunks)
            
        except Exception as e:
            logger.error(f"長文翻訳エラー: {e}")
            return None


def main():
    """テスト実行"""
    translator = MeduzaTranslator()
    
    # テスト用ロシア語テキスト
    test_text = "Россия и Украина ведут переговоры о мире."
    
    result = translator.translate_text(test_text)
    if result:
        print(f"原文: {test_text}")
        print(f"翻訳: {result}")
    else:
        print("翻訳に失敗しました")


if __name__ == "__main__":
    main()
