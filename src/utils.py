"""
補助関数・ユーティリティ
共通で使用する関数やヘルパー
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
import re

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None):
    """
    ログ設定をセットアップ
    
    Args:
        log_level (str): ログレベル
        log_file (Optional[str]): ログファイルパス
    """
    level = getattr(logging, log_level.upper(), logging.INFO)
    
    handlers = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(log_file))
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=handlers
    )


def save_json(data: Any, filepath: str) -> bool:
    """
    データをJSONファイルに保存
    
    Args:
        data: 保存するデータ
        filepath (str): ファイルパス
        
    Returns:
        bool: 保存成功フラグ
    """
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"JSONファイル保存完了: {filepath}")
        return True
        
    except Exception as e:
        logger.error(f"JSONファイル保存エラー: {e}")
        return False


def load_json(filepath: str) -> Optional[Any]:
    """
    JSONファイルからデータを読み込み
    
    Args:
        filepath (str): ファイルパス
        
    Returns:
        Optional[Any]: 読み込んだデータ
    """
    try:
        if not os.path.exists(filepath):
            logger.warning(f"ファイルが存在しません: {filepath}")
            return None
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        logger.info(f"JSONファイル読み込み完了: {filepath}")
        return data
        
    except Exception as e:
        logger.error(f"JSONファイル読み込みエラー: {e}")
        return None


def clean_text(text: str) -> str:
    """
    テキストをクリーニング
    
    Args:
        text (str): クリーニング対象のテキスト
        
    Returns:
        str: クリーニング済みテキスト
    """
    if not text:
        return ""
    
    # HTMLタグを除去
    text = re.sub(r'<[^>]+>', '', text)
    
    # 余分な空白を除去
    text = re.sub(r'\s+', ' ', text)
    
    # 前後の空白を除去
    text = text.strip()
    
    return text


def format_timestamp(timestamp: str = None) -> str:
    """
    タイムスタンプをフォーマット
    
    Args:
        timestamp (str): タイムスタンプ（None の場合は現在時刻）
        
    Returns:
        str: フォーマット済みタイムスタンプ
    """
    if timestamp is None:
        dt = datetime.now()
    else:
        try:
            # 一般的なRSSタイムスタンプ形式を想定
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        except:
            dt = datetime.now()
    
    return dt.strftime('%Y-%m-%d %H:%M:%S')


def create_safe_filename(text: str, max_length: int = 100) -> str:
    """
    安全なファイル名を作成
    
    Args:
        text (str): 元のテキスト
        max_length (int): 最大文字数
        
    Returns:
        str: 安全なファイル名
    """
    # 使用できない文字を除去
    safe_text = re.sub(r'[<>:"/\\|?*]', '', text)
    
    # 最大文字数で切り詰め
    if len(safe_text) > max_length:
        safe_text = safe_text[:max_length]
    
    # 空白をアンダースコアに変換
    safe_text = safe_text.replace(' ', '_')
    
    return safe_text


def validate_url(url: str) -> bool:
    """
    URLの妥当性をチェック
    
    Args:
        url (str): チェック対象のURL
        
    Returns:
        bool: 妥当性フラグ
    """
    url_pattern = re.compile(
        r'^https?://'  # スキーム
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # ドメイン
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
        r'(?::\d+)?'  # ポート
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return url_pattern.match(url) is not None


class ConfigManager:
    """設定管理クラス"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self) -> Dict:
        """設定を読み込み"""
        default_config = {
            "rss_url": "https://meduza.io/rss/all",
            "translation": {
                "source_lang": "ru",
                "target_lang": "ja",
                "delay": 1.0
            },
            "output": {
                "format": "json",
                "directory": "output"
            }
        }
        
        config = load_json(self.config_file)
        if config is None:
            logger.info("デフォルト設定を使用します")
            self.save_config(default_config)
            return default_config
        
        return config
    
    def save_config(self, config: Dict = None) -> bool:
        """設定を保存"""
        if config is None:
            config = self.config
        
        return save_json(config, self.config_file)
    
    def get(self, key: str, default: Any = None) -> Any:
        """設定値を取得"""
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default


def main():
    """テスト実行"""
    # ログ設定テスト
    setup_logging("DEBUG")
    
    # 設定管理テスト
    config = ConfigManager()
    print(f"RSS URL: {config.get('rss_url')}")
    print(f"翻訳遅延: {config.get('translation.delay')}")
    
    # テキストクリーニングテスト
    dirty_text = "<p>  これは  テスト  です  </p>"
    clean = clean_text(dirty_text)
    print(f"クリーニング前: {dirty_text}")
    print(f"クリーニング後: {clean}")


if __name__ == "__main__":
    main()
