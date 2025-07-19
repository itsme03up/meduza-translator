#!/usr/bin/env python3
"""
Meduza Translator - メインエントリーポイント
"""
from src.fetch_articles import fetch_meduza_articles

def main():
    articles = fetch_meduza_articles(limit=5)
    for i, art in enumerate(articles, 1):
        print(f"[{i}] {art['title']}")
        print(f"URL: {art['link']}")
        print(f"日付: {art['published']}")
        print("-" * 40)


if __name__ == "__main__":
    main()
