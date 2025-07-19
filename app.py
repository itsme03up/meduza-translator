import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
from src.fetch_articles import fetch_meduza_articles
from src.translate import MeduzaTranslator
from src.summarize import summarize_article
from src.database import init_db, save_article_to_db

DB_PATH = "data/articles.db"

def get_translated_articles(search_query="", date_filter="all", limit=20):
    """翻訳済みの記事一覧を取得"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    query = """
        SELECT translated_title, summary, translated_content, published, title
        FROM articles 
        WHERE translated_title IS NOT NULL
    """
    params = []
    
    # 検索クエリ
    if search_query:
        query += " AND (translated_title LIKE ? OR summary LIKE ? OR translated_content LIKE ?)"
        search_param = f"%{search_query}%"
        params.extend([search_param, search_param, search_param])
    
    # 日付フィルター
    if date_filter == "today":
        today = datetime.now().strftime('%Y-%m-%d')
        query += " AND date(published) = ?"
        params.append(today)
    elif date_filter == "week":
        week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        query += " AND date(published) >= ?"
        params.append(week_ago)
    elif date_filter == "month":
        month_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        query += " AND date(published) >= ?"
        params.append(month_ago)
    
    query += " ORDER BY published DESC LIMIT ?"
    params.append(limit)
    
    cursor.execute(query, params)
    articles = cursor.fetchall()
    conn.close()
    return articles

def get_article_stats():
    """記事統計を取得"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 総記事数
    cursor.execute("SELECT COUNT(*) FROM articles")
    total_count = cursor.fetchone()[0]
    
    # 翻訳済み記事数
    cursor.execute("SELECT COUNT(*) FROM articles WHERE translated_title IS NOT NULL")
    translated_count = cursor.fetchone()[0]
    
    # 今日の記事数
    today = datetime.now().strftime('%Y-%m-%d')
    cursor.execute("SELECT COUNT(*) FROM articles WHERE date(published) = ?", (today,))
    today_count = cursor.fetchone()[0]
    
    conn.close()
    return total_count, translated_count, today_count

def fetch_and_process_new_articles(num_articles=3):
    """新着記事を取得して処理する"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # データベース初期化
        init_db()
        
        # 記事取得
        status_text.text("📰 新着記事を取得中...")
        progress_bar.progress(20)
        articles = fetch_meduza_articles(limit=num_articles)
        
        if not articles:
            st.error("記事の取得に失敗しました")
            return False
        
        # 翻訳器初期化
        translator = MeduzaTranslator()
        
        for i, article in enumerate(articles):
            progress = 20 + (i + 1) * (80 / len(articles))
            
            # 翻訳
            status_text.text(f"🌐 記事 {i+1}/{len(articles)} を翻訳中...")
            progress_bar.progress(int(progress * 0.6))
            
            translated = translator.translate_article(article)
            
            # 要約
            status_text.text(f"📝 記事 {i+1}/{len(articles)} を要約中...")
            progress_bar.progress(int(progress * 0.8))
            
            if translated.get('translated_content'):
                summary = summarize_article(translated['translated_content'])
                translated['summary'] = summary
            
            # 保存
            status_text.text(f"💾 記事 {i+1}/{len(articles)} を保存中...")
            save_article_to_db(translated)
            progress_bar.progress(int(progress))
        
        progress_bar.progress(100)
        status_text.text("✅ 処理完了！")
        return True
        
    except Exception as e:
        st.error(f"エラーが発生しました: {str(e)}")
        return False

# --- Streamlit UI ---
st.set_page_config(
    page_title="Meduza翻訳記事ビューア", 
    layout="wide",
    page_icon="📰"
)

st.title("📰 Meduza翻訳記事ビューア")
st.markdown("---")

# サイドバー：コントロールパネル
with st.sidebar:
    st.header("🎛️ コントロールパネル")
    
    # 統計情報
    total_count, translated_count, today_count = get_article_stats()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("総記事数", total_count)
        st.metric("今日の記事", today_count)
    with col2:
        st.metric("翻訳済み", translated_count)
        if total_count > 0:
            st.metric("翻訳率", f"{translated_count/total_count*100:.1f}%")
    
    st.markdown("---")
    
    # 新着記事取得
    st.subheader("🆕 新着記事取得")
    num_articles = st.selectbox("取得記事数", [1, 3, 5, 10], index=1)
    
    if st.button("🔄 新着記事を取得・翻訳", type="primary"):
        with st.spinner("処理中..."):
            if fetch_and_process_new_articles(num_articles):
                st.success(f"✅ {num_articles}件の記事を処理しました！")
                st.rerun()
    
    st.markdown("---")
    
    # 検索・フィルター
    st.subheader("🔍 検索・フィルター")
    search_query = st.text_input("キーワード検索", placeholder="記事のタイトルや内容を検索...")
    
    date_filter = st.selectbox(
        "期間フィルター",
        ["all", "today", "week", "month"],
        format_func=lambda x: {
            "all": "全期間",
            "today": "今日",
            "week": "1週間以内",
            "month": "1ヶ月以内"
        }[x]
    )
    
    display_limit = st.selectbox("表示件数", [10, 20, 50, 100], index=1)

# メインコンテンツ
articles = get_translated_articles(search_query, date_filter, display_limit)

if not articles:
    st.warning("条件に一致する記事が見つかりません。")
    st.info("💡 「新着記事を取得・翻訳」ボタンで記事を追加してください。")
else:
    st.success(f"📊 {len(articles)}件の記事が見つかりました")
    
    # 記事表示オプション
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        view_mode = st.radio("表示モード", ["カード表示", "リスト表示"], horizontal=True)
    with col2:
        show_content = st.checkbox("本文を表示", value=False)
    with col3:
        st.download_button(
            "📥 CSVダウンロード",
            pd.DataFrame(articles, columns=["翻訳タイトル", "要約", "翻訳本文", "公開日", "原題"]).to_csv(index=False),
            "meduza_articles.csv",
            "text/csv"
        )
    
    st.markdown("---")
    
    # 記事表示
    if view_mode == "カード表示":
        for idx, (translated_title, summary, content, published, original_title) in enumerate(articles, 1):
            with st.expander(f"📰 {idx}. {translated_title} ({published})"):
                
                # 原題
                st.caption(f"🇷🇺 原題: {original_title}")
                
                # 要約
                if summary:
                    st.write("### 📝 要約")
                    st.info(summary)
                
                # 本文
                if show_content and content:
                    st.write("### 📖 本文")
                    st.write(content)
                elif not show_content:
                    st.caption("💡 本文を表示するには「本文を表示」をチェックしてください")
    
    else:  # リスト表示
        for idx, (translated_title, summary, content, published, original_title) in enumerate(articles, 1):
            st.write(f"**{idx}. {translated_title}**")
            st.caption(f"📅 {published} | 🇷🇺 {original_title}")
            
            if summary:
                st.write(f"📝 {summary[:200]}..." if len(summary) > 200 else summary)
            
            if show_content and content:
                with st.expander("本文を読む"):
                    st.write(content)
            
            st.markdown("---")

# フッター
st.markdown("---")
st.markdown(
    "🔗 **Meduza翻訳記事ビューア** | "
    "データソース: [Meduza.io](https://meduza.io) | "
    f"最終更新: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
)
