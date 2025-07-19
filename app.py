import streamlit as st
import sqlite3

DB_PATH = "articles.db"

def get_translated_articles():
    """翻訳済みの記事一覧を取得"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT title_ja, summary_ja, content_ja, published 
        FROM articles 
        ORDER BY published DESC 
        LIMIT 10
    """)
    articles = cursor.fetchall()
    conn.close()
    return articles

# --- Streamlit UI ---
st.set_page_config(page_title="Meduza翻訳記事ビューア", layout="wide")
st.title("📰 Meduza翻訳記事ビューア")

articles = get_translated_articles()

if not articles:
    st.warning("まだ記事が翻訳されていません。")
else:
    for idx, (title, summary, content, published) in enumerate(articles, 1):
        with st.expander(f"{idx}. {title}（{published}）"):
            st.write("### 📝 要約")
            st.write(summary or "（要約なし）")
            st.write("### 📖 本文")
            st.write(content or "（本文なし）")
