# Meduza Translator

ロシア語ニュースサイト「Медуза」から最新記事を取得し、日本語に翻訳するPythonアプリです。

## 🔧 セットアップ

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

# 📂 ステップ2：.gitignore を作成

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

