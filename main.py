#!/usr/bin/env python3
"""
Meduza Translator - メインエントリーポイント
"""
from src.fetch_articles import fetch_meduza_articles
from src.translate import MeduzaTranslator
from src.summarize import summarize_article
from src.database import init_db, save_article_to_db

def main():
    # データベース初期化
    init_db()
    
    # 記事取得
    print("📰 Meduza記事を取得中...")
    articles = fetch_meduza_articles(limit=3)
    
    # 翻訳器初期化
    translator = MeduzaTranslator()

    for i, article in enumerate(articles, 1):
        print(f"\n=== 記事 {i}/{len(articles)} ===")
        print(f"原題: {article['title']}")
        
        # 翻訳
        print("🌐 翻訳中...")
        translated = translator.translate_article(article)
        print(f"和訳: {translated.get('translated_title', '翻訳失敗')}")
        
        # 要約
        print("📝 要約作成中...")
        summary = summarize_article(translated.get('translated_content', ''))
        translated['summary'] = summary
        print(f"要約: {summary[:100]}..." if summary else "要約失敗")
        
        # 保存
        print("💾 データベースに保存中...")
        save_article_to_db(translated)
        print("✅ 保存完了")

    print(f"\n🎉 {len(articles)}件の記事処理が完了しました！")

if __name__ == "__main__":
    main()