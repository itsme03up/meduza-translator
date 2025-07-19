# src/database.py

import sqlite3
from datetime import datetime
from typing import Optional, Dict

DB_PATH = "articles.db"

def init_db():
    """初期テーブルを作成（初回のみ呼び出す）"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT,
        summary TEXT,
        content TEXT,
        translated_title TEXT,
        translated_summary TEXT,
        translated_content TEXT,
        content_ja TEXT,
        summary_auto TEXT,
        translated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    conn.commit()
    conn.close()


def get_or_create_user(username: str) -> int:
    """ユーザーIDを取得（なければ新規作成）"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("INSERT OR IGNORE INTO users (username) VALUES (?)", (username,))
    conn.commit()

    cur.execute("SELECT id FROM users WHERE username = ?", (username,))
    user_id = cur.fetchone()[0]

    conn.close()
    return user_id


def save_article(username: str, title: str, content: str, summary: Optional[str]):
    """記事を保存する"""
    user_id = get_or_create_user(username)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO articles (user_id, title, content_ja, summary_auto)
    VALUES (?, ?, ?, ?)
    """, (user_id, title, content, summary))

    conn.commit()
    conn.close()

def save_article_to_db(article: Dict, db_path="articles.db") -> None:
    """記事データをSQLiteに保存"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO articles (title, summary, content, translated_title, translated_summary, translated_content, summary_auto)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        article.get("title"),
        article.get("summary"),
        article.get("content"),
        article.get("title_ja"),
        article.get("summary_ja"),
        article.get("content_ja"),
        article.get("summary_auto")
    ))
    
    conn.commit()
    conn.close()
