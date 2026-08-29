# 地図のピンをクリックしたら詳細ページに遷移するように変更

日付: 2026-08-29

## これは何をする作業か

それまで地図には東京駅の位置に固定のマーカーが1つ表示されるだけだった。DBに登録された全てのゴミ箱を地図上にピンとして表示し、ピンをクリックするとそのゴミ箱の詳細ページに飛べるようにする。

## 手順

1. `trash_map/app.py` に、ゴミ箱1件の詳細を表示するページのルートを追加する。
   ```python
   @app.route("/trash/<int:trash_id>")
   def detail_page(trash_id):
       trash_can = db.get_or_404(TrashCan, trash_id)
       type_labels = [GARBAGE_TYPE_LABELS.get(key, key) for key in trash_can.type.split(",")]
       return render_template("trash/detail.html", item=trash_can, type_labels=type_labels)
   ```
   `db.get_or_404(...)` を使うと、指定したIDのデータが存在しない場合に自動的に404エラーページが返る（`if trash_can is None: abort(404)` のような分岐を自分で書く必要がない）。
2. 同じく `trash_map/app.py` に、地図のJavaScriptがゴミ箱データを取得するための窓口（API）を追加する。
   ```python
   @app.route("/api/trashcans")
   def api_trashcans():
       trash_cans = TrashCan.query.all()
       return {"items": [{"id": t.id, "name": t.name, "latitude": t.latitude, "longitude": t.longitude} for t in trash_cans]}
   ```
   Flaskは辞書（dict）を返すと自動的にJSON形式に変換してくれる。
3. `trash_map/templates/trash/detail.html` を、存在しないフィールド `item.coordinate` を使っていた旧実装から、実際に存在するフィールド（`name` / `postal_code` / `address` / `latitude` / `longitude` / `photo_filename`）を表示する内容に書き換える。`type`（カンマ区切りの英語キー）は、ビュー側で日本語ラベルのリストに変換してから `type_labels | join('、')` で「、」区切りの読みやすい形にして表示する。
4. `trash_map/templates/map/map.html` を、DBと連携する形に変更する。
   - ハードコードされていた東京駅の固定マーカー（`L.marker([35.681236, 139.767125]).bindPopup("東京駅")`）を削除する。
   - ページが読み込まれたときに `fetch("/api/trashcans")` でDBの全ゴミ箱データを取得し、それぞれの座標にマーカーを作る。
   - マーカーに `bindTooltip(item.name)` を設定し、マウスを乗せると名前が表示されるようにする。
   - マーカーの `click` イベントで `window.location.href = '/trash/${item.id}'` を実行し、ピンをクリックすると該当ゴミ箱の詳細ページに遷移するようにする。

## 動作確認

1. `/api/trashcans` にアクセスし、登録済みのゴミ箱（サンプル1件）がJSON形式で返ることを確認する。
2. `/trash/1` にアクセスし、実際のデータ（名前・写真・種別ラベル）付きで `200` が返ることを確認する。
3. 存在しないID（例: `/trash/9999`）にアクセスし、`404` が返ることを確認する。
4. `/map` のHTMLソースを確認し、`fetch("/api/trashcans")` とマーカー生成・クリック時遷移のスクリプトが正しく出力されていることを確認する。
