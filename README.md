# Meduza Translator 📰

ロシア語ニュースサイト「Медуза」から最新記事を取得し、日本語に翻訳・要約するStreamlitアプリです。

## 🚀 ライブデモ
[Streamlit Cloud でアプリを見る](https://meduza-translator-dndc7zngz5jralyhlz7ojm.streamlit.app/) (デプロイ後に更新)

## ✨ 機能

✅ **記事取得**: МедузаのRSSから最新記事を自動取得  
✅ **自動翻訳**: ロシア語→日本語への高精度翻訳  
✅ **自動要約**: 長文記事の要点を抽出  
✅ **検索・フィルター**: キーワード検索、日付範囲絞り込み  
✅ **美しいUI**: Streamlitによる直感的なインターフェース  
✅ **データ永続化**: SQLiteによる記事データベース  

## 🎯 プロジェクトの目的

- ロシア語学習者にとって、**ニュース記事の読解は難度が高い**が、非常に有益な教材である
- 機械翻訳と要約を組み合わせることで、**記事理解のハードルを下げる**
- 最新のニュースを通じて、**生きたロシア語に触れる機会を提供**

## 📋 実装済み機能

| 機能カテゴリ | ステータス | 説明 |
|--------------|------------|------|
| ✅ ニュース取得 | 完了 | МедузаのRSSから最新記事を取得 |
| ✅ 本文抽出 | 完了 | Beautiful Soupによる記事本文スクレイピング |
| ✅ 翻訳 | 完了 | googletransによるロシア語→日本語翻訳 |
| ✅ 要約 | 完了 | sumyライブラリによる自動要約生成 |
| ✅ データ保存 | 完了 | SQLiteデータベースによる記事管理 |
| ✅ Web UI | 完了 | Streamlitによる直感的なインターフェース |
| ✅ 検索機能 | 完了 | キーワード検索・日付フィルター |

## �️ 技術スタック

| 技術 | 用途 | 理由 |
|------|------|------|
| **Streamlit** | WebアプリUI | 簡単にWebアプリが作れる |
| **googletrans** | 自動翻訳 | 無料で使え、精度も実用的 |
| **feedparser** | RSS解析 | Meduzaの記事フィード取得 |
| **BeautifulSoup** | HTML解析 | 記事本文の抽出 |
| **sumy** | 文書要約 | 高精度な自動要約 |
| **SQLite** | データベース | 軽量で設定不要 |
| `feedparser` | RSSパース | Медуза公式RSSフィードを安全に取得 |
| `requests` + `BeautifulSoup` | 記事本文の抽出（予定） | ページ内の本文をHTMLから取得するため |
| `sqlite3`（予定） | 学習履歴・語彙の保存 | 軽量・構成が簡単でポートフォリオに最適 |
| `Python 3.11+` | 実装全体 | 学校・就活でもよく使われるスタンダード |
| `venv` | 仮想環境管理 | 開発環境を汚さずにパッケージ管理可能 |

---

## 🧠 ポートフォリオとしての狙い

- 実用性のある「語学 × 技術」テーマで**ユニークさをアピール**
- スクレイピング / 自然言語処理 / 翻訳 / データベース管理など、**幅広いスキルを統合**
- 今後、StreamlitやFlaskによる**GUI化や可視化**に発展可能
- 自己学習にも実用できる、**等身大のプロジェクト**として仕上げる

---

## 📦 今後の拡張予定

- [ ] 記事要約機能（sumy / transformers等の導入）
- [ ] 語彙自動抽出＆記録（DB連携）
- [ ] StreamlitでGUI化
- [ ] 読んだ記事の復習タイマー（忘却曲線ロジック）

---

## 🔧 セットアップ手順

```bash
git clone https://github.com/yourname/meduza-translator.git
cd meduza-translator
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
🚀 使い方
bash
コピーする
編集する
python main.py
📦 使用ライブラリ
googletrans 4.0.0-rc1

feedparser

requests

beautifulsoup4

📝 ライセンス
MIT

yaml
コピーする
編集する

---

##ディレクトリ構成
meduza-translator/
├── main.py                    # 実行用エントリーポイント
├── README.md
├── requirements.txt
├── .gitignore
├── venv/                      # 仮想環境（git管理外）
├── data/                      # ローカル保存用データ（任意）
│   └── articles.db            # 今後のSQLite用
├── src/                       # ソースコードフォルダ
│   ├── __init__.py
│   ├── fetch_articles.py      # RSS取得ロジック
│   ├── translate.py           # 翻訳処理（googletrans）
│   ├── summarize.py           # 要約処理（予定）
│   └── utils.py               # 補助関数など
└── tests/                     # 単体テスト（後から追加してもOK）
    └── test_fetch_articles.py


### 🔧 コマンド：

```bash
touch .gitignore
✍️ 内容（Pythonプロジェクト標準）：
gitignore
コピーする
編集する
# Pythonキャッシュ
__pycache__/
*.pyc

# 仮想環境
venv/

# 環境変数ファイル（もし使うなら）
.env

# VSCodeなどエディタの設定
.vscode/
.idea/
✅ ステップ3：Gitに追加して初回コミット
bash
コピーする
編集する
git init
git add .
git commit -m "🎉 初期コミット: 仮想環境・README・.gitignore追加"
（リモートにまだGitHubを連携していない場合、あとでリモート追加する）

