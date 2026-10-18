# 環境構築（フロントエンド編）

> [フロントエンド編](../../01_frontend/)を始める前に行います。最初の章は[01_frontend/01_html_basics](../../01_frontend/01_html_basics/)です。バックエンド編に進むときは、[backend.md](backend.md)の手順を追加で行います。

フロントエンド編で使うブラウザ・VS Code・拡張機能を用意します。HTML・CSS・JavaScriptは、ブラウザとテキストエディタがあれば動くので、バックエンド編のようなライブラリのインストールはありません。Pythonは、10_js_dataの章から「簡易サーバー」を起動するためだけに使います。

## 目次

1. [ブラウザを用意する](#ブラウザを用意する)
2. [VS Codeを入れる](#vs-codeを入れる)
3. [VS Codeの拡張機能を入れる](#vs-codeの拡張機能を入れる)
4. [Pythonを用意する（10_js_dataから）](#pythonを用意する10_js_dataから)
5. [Gitを用意する（11_homepageの公開をするときだけ）](#gitを用意する11_homepageの公開をするときだけ)
6. [動作確認](#動作確認)

---

## ブラウザを用意する

**Google Chrome**をおすすめします。このカリキュラムの「開発者ツール」の説明（Elements・Console・Networkなどのパネルの名前や、ショートカットキー）は、Chromeに合わせています。Edgeも中身はChromeと同じ仕組みなので、ほぼ同じように使えます。

- ダウンロード：<https://www.google.com/chrome/>

インストールしたら、どこかのWebページを開き、**開発者ツール**を開けるか確かめます。HTML・CSS・JavaScriptの学習で一番使う道具です（使い方は[01_frontend/01_html_basics](../../01_frontend/01_html_basics/#0-はじめに学習環境と開発者ツール)の0節）。

| OS | 開発者ツールを開くキー |
|---|---|
| Mac | `Cmd + Option + I` |
| Windows | `F12`（または`Ctrl + Shift + I`） |

SafariやFirefoxは、完成したページが他のブラウザでも崩れないかを確かめるとき（[01_frontend/11_homepage](../../01_frontend/11_homepage/)の3節）に使います。

---

## VS Codeを入れる

コードを書くエディタとして、**Visual Studio Code**（VS Code）を使います。

- ダウンロード：<https://code.visualstudio.com/>

インストールしたら、このリポジトリのフォルダを開きます。

1. VS Codeの「ファイル」→「フォルダーを開く」（Mac：「File」→「Open Folder」）
2. このリポジトリのフォルダ（`README.md`・`01_frontend/`・`02_backend/`があるフォルダ）を選ぶ
3. 左側のエクスプローラーに、フォルダとファイルの一覧が表示される

ターミナル（コマンドを打つ画面）は、「表示」→「ターミナル」（ショートカットは`` Ctrl + ` ``。`` ` ``はバッククォート）で、VS Codeの下側に開けます。

---

## VS Codeの拡張機能を入れる

VS Codeの左端の、四角が4つ並んだアイコン（拡張機能）から、名前で検索してインストールします。

| 拡張機能 | 発行元 | できること |
|---|---|---|
| Japanese Language Pack for Visual Studio Code | Microsoft | VS Codeのメニューを日本語にする（任意）。インストール後、右下の`Change Language and Restart`を押す |
| Live Server | Ritwick Dey | `.html`ファイルを、保存するたびに自動で再読み込みしながらブラウザで表示する |

**Live Serverの使い方**：`.html`ファイルをエディタで開いた状態で、右クリック →`Open with Live Server`を選ぶと、ブラウザで`http://127.0.0.1:5500/…`が開きます。以後、ファイルを保存するたびにブラウザが自動で更新されます。止めるときは、VS Codeの右下の`Port : 5500`を押します。

そのほかの便利な拡張機能と使い方は、[vscode.md](vscode.md)にまとめています。

---

## Pythonを用意する（10_js_dataから）

[01_frontend/10_js_data](../../01_frontend/10_js_data/)からは、`fetch()`でJSONファイルを読み込むため、ページを`file://`ではなく`http://`で開く必要があります。そのための**簡易サーバー**を、Pythonで起動します（Pythonのプログラムを書くわけではありません）。

ターミナルで、Pythonが入っているかを確かめます。

```bash
python3 --version     # Mac
python --version      # Windows
```

`Python 3.10`以上が表示されればOKです（バックエンド編でも3.10以上を使います）。表示されないときは、[python.org](https://www.python.org/downloads/)からインストールします（Windowsでは、インストーラーの最初の画面で「Add python.exe to PATH」にチェックを入れます）。

簡易サーバーは、次のように起動します（Macで`python`が見つからない場合は`python3`と打ちます）。

```bash
cd 01_frontend/10_js_data
python -m http.server 8000
# → ブラウザで http://localhost:8000/ を開く（止めるときは Ctrl + C）
```

Live Serverで開いたページも`http://127.0.0.1:5500/…`なので、`fetch()`が動きます。どちらを使っても構いません。

フロントエンド編では、Pythonのライブラリのインストールや仮想環境は必要ありません。

---

## Gitを用意する（11_homepageの公開をするときだけ）

[01_frontend/11_homepage](../../01_frontend/11_homepage/#補足github-pagesで公開する)の補足で、作ったオリジナルHPをGitHub Pagesで公開するときに、**Git**と**GitHubのアカウント**を使います。公開しない場合は不要です。

インストールとGitHubへのpushの手順は、[github/README.md](../github/)にまとめています。

---

## 動作確認

| 確認する操作 | 確認したいこと |
|---|---|
| Chromeで好きなWebページを開き、開発者ツールを開く | Elements・Console・Networkなどのタブが表示される |
| VS Codeで[01_frontend/01_html_basics/example/01_structure/index.html](../../01_frontend/01_html_basics/example/01_structure/index.html)を開き、右クリック →`Open with Live Server` | ブラウザでページが開く。`<h1>`の文字を書き換えて保存すると、ブラウザの表示も自動で変わる（確認後は元に戻す） |
| ターミナルで`cd 01_frontend/10_js_data`→`python -m http.server 8000`を実行し、<http://localhost:8000/example/02_fetch/index.html>を開く | ページが表示され、「data/memos.json を読み込む」を押すとメモが表示される |

すべて確認できたら、[01_frontend/01_html_basics](../../01_frontend/01_html_basics/)から始めましょう。Webページが表示されるしくみは、[web_basic](../web_basic/)で必要なときに確かめられます。
