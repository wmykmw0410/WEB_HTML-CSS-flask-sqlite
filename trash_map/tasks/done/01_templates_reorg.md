# `templates/` を機能別に再構成

日付: 2026-08-29

## これは何をする作業か

それまで `templates/` 直下に全ページのHTMLファイルが並んでいて、どれが何のページか分かりにくかった。役割ごとにサブフォルダへ移動し、見通しを良くする。

## 手順

1. ターミナルで `trash_map/templates` に移動する。
   ```bash
   cd trash_map/templates
   ```
2. 役割ごとのサブフォルダを作る。
   ```bash
   mkdir -p map trash error draft
   ```
3. 既存のHTMLファイルを該当フォルダへ移動する。
   ```bash
   mv map.html map/
   mv add.html thankyou.html list.html detail.html trash/
   mv wrong.html error/
   mv home.html burnable.html draft/
   ```
   移動後の対応関係:

   | 移動前 | 移動後 | 用途 |
   |---|---|---|
   | `map.html` | `map/map.html` | 地図表示 |
   | `add.html` | `trash/add.html` | ゴミ箱登録フォーム |
   | `thankyou.html` | `trash/thankyou.html` | 登録完了 |
   | `list.html` | `trash/list.html` | 一覧（ルート未実装） |
   | `detail.html` | `trash/detail.html` | 詳細（ルート未実装） |
   | `wrong.html` | `error/wrong.html` | エラー表示 |
   | `home.html` | `draft/home.html` | 未使用プレースホルダー |
   | `burnable.html` | `draft/burnable.html` | 未使用プレースホルダー |
4. ファイルを移動すると、`render_template()` に渡していたパスが古いままではエラーになる。`trash_map/app.py` を開き、以下の箇所を書き換える。
   - `map_page` 内: `render_template("map.html")` → `render_template("map/map.html")`
   - `index_page` 内: `render_template("map.html")` → `render_template("map/map.html")`
   - `add_page` 内: `render_template("add.html", form=form)` → `render_template("trash/add.html", form=form)`
   - `thankyou_page` 内: `render_template("thankyou.html")` → `render_template("trash/thankyou.html")`

## 動作確認

1. 以下を実行し、主要ページが `200`（正常）を返すことを確認する。
   ```bash
   flaskenv/bin/python -c "
   import app
   client = app.app.test_client()
   for path in ['/', '/map', '/add', '/thankyou']:
       r = client.get(path)
       print(path, r.status_code)
   "
   ```
2. `/`, `/map`, `/add`, `/thankyou` すべて `200` を返すことを確認済み。

（注: `draft/` フォルダは後日、どこからも参照されていないことを確認した上で削除済み）
