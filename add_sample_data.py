import streamlit as st
from src.fetch_articles import fetch_meduza_articles
from src.translate import MeduzaTranslator
from src.summarize import summarize_article

def add_sample_data():
    """サンプルデータを追加"""
    sample_articles = [
        {
            'title': 'Привет, мир!',
            'translated_title': 'こんにちは、世界！',
            'content': 'Это тестовая статья для демонстрации работы приложения.',
            'translated_content': 'これは、アプリケーションの動作を実演するためのテスト記事です。',
            'summary': 'テストアプリケーションのデモンストレーション記事',
            'published': '2025-07-19T16:00:00+03:00'
        },
        {
            'title': 'Новости дня',
            'translated_title': '今日のニュース',
            'content': 'Сегодня произошло много интересных событий в мире.',
            'translated_content': '今日、世界では多くの興味深い出来事が起こりました。',
            'summary': '世界の興味深い出来事に関する日報',
            'published': '2025-07-19T15:30:00+03:00'
        }
    ]
    
    if 'articles' not in st.session_state:
        st.session_state.articles = []
    
    for article in sample_articles:
        existing_titles = [a.get('translated_title', '') for a in st.session_state.articles]
        if article['translated_title'] not in existing_titles:
            st.session_state.articles.append(article)

if __name__ == "__main__":
    add_sample_data()
    print("サンプルデータを追加しました")
