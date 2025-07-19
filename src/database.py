# src/database.py

import sqlite3
import os
from datetime import datetime
from typing import Optional, Dict

DB_PATH = "data/articles.db"

def init_db():
    """初期テーブルを作成（初回のみ呼び出す）"""
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        content TEXT,
        translated_title TEXT,
        translated_content TEXT,
        summary TEXT,
        published TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_article_to_db(article: Dict, db_path="data/articles.db") -> None:
    """記事データをSQLiteに保存"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO articles (title, content, translated_title, translated_content, summary, published)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        article.get("title"),
        article.get("content"),
        article.get("translated_title"),
        article.get("translated_content"),
        article.get("summary"),
        article.get("published")
    ))
    
    conn.commit()
    conn.close()
