#!/usr/bin/env python3
"""
Meduza Translator - メインエントリーポイント
"""
from src.fetch_articles import fetch_meduza_articles
from src.translate import MeduzaTranslator

def main():
    articles = fetch_meduza_articles(limit=5)
    translator = MeduzaTranslator()

    for i, article in enumerate(articles):
        print(f"\n=== 記事 {i+1} ===")
        print(f"原題: {article['title']}")
        translated = translator.translate_article(article)
        print(f"和訳: {translated.get('title_ja', '翻訳失敗')}")

if __name__ == "__main__":
    main()