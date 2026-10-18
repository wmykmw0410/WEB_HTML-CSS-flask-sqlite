# 00_docs（補足資料）

フロントエンド編・バックエンド編を進めるときに、横に置いて使う資料です。章のように順番に読む必要はありません。

## フォルダ構成

```
00_docs/
├── setup/              環境構築
│   ├── frontend.md       フロントエンド編の環境構築（ブラウザ・VS Code・Live Server）
│   ├── backend.md        バックエンド編の環境構築（Python・仮想環境・ライブラリ）
│   ├── vscode.md         VS Codeのおすすめ拡張機能と使い方
│   └── requirements.txt  バックエンド編で使うライブラリの一覧
├── web_basic/          Webページが表示されるしくみ（リクエストとレスポンス・URL・ステータスコード・HTTPS・IPアドレス）
├── glossary/           用語集（章をまたいで出てくる用語）
├── python_grammar/     Pythonの文法リファレンス（基礎・中級・発展）
└── github/             GitHubにリポジトリをpushする手順
```

## いつ読むか

| 資料 | 読むタイミング |
|---|---|
| [setup/frontend.md](setup/frontend.md) | フロントエンド編を始める前に、1回だけ |
| [setup/backend.md](setup/backend.md) | バックエンド編を始める前に、1回だけ。ライブラリは[setup/requirements.txt](setup/requirements.txt)でまとめてインストールする |
| [setup/vscode.md](setup/vscode.md) | VS Codeの拡張機能を足したくなったとき |
| [web_basic/](web_basic/) | URL・リクエストとレスポンス・ステータスコードなど、Webのしくみの言葉が出てきたとき。フロントエンド編を始める前に一度ざっと読んでおくと、全体像がつかみやすい |
| [glossary/](glossary/) | 章の中で、意味を忘れた用語が出てきたとき |
| [python_grammar/](python_grammar/) | バックエンド編で、わからないPythonの文法が出てきたとき |
| [github/](github/) | 作ったものをGitHubに置きたくなったとき（フロントエンド編の[11_homepage](../01_frontend/11_homepage/)でHPを公開するときなど） |
