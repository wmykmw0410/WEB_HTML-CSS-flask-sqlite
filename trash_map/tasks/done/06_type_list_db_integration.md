# ゴミ種別ごとの一覧ページをDBと連携

日付: 2026-08-29

## これは何をする作業か

前段（`05_hamburger_menu.md`）で作った `/list/<type_key>` は「準備中です」と表示するだけの仮実装だった。実際にデータベースから該当するゴミ箱を検索して表示するように変更する。

## 手順

1. `trash_map/app.py` の `type_list_page` 関数を、DBから該当種別のゴミ箱だけを絞り込む処理に書き換える。
   ```python
   @app.route("/list/<type_key>")
   def type_list_page(type_key):
       label = GARBAGE_TYPE_LABELS.get(type_key, type_key)
       items = [
           trash_can for trash_can in TrashCan.query.all()
           if type_key in trash_can.type.split(",")
       ]
       return render_template("trash/type_list.html", label=label, items=items)
   ```
   **なぜ `type.like(f'%{type_key}%')` のようなSQL検索を使わないのか:**
   `type` カラムはカンマ区切り文字列（例: `"burnable,can"`）で保存されている。もし `LIKE '%burnable%'` のような部分一致検索をすると、`"burnable"` という文字列は `"nonburnable"`（不燃ごみ）の中にも含まれてしまうため、燃えるゴミの一覧に不燃ごみが紛れ込んでしまう。これを避けるため、Python側で `type.split(",")` によってカンマで区切ったリストにしてから、「リストの中に完全に一致する要素があるか」をチェックしている。
2. `trash_map/templates/trash/type_list.html` を、「準備中です」の固定表示から、実際のデータを表示するテーブルに書き換える。`items` が1件以上あればテーブル（名前・住所・緯度・経度）を表示し、0件なら「登録されている{{ label }}のゴミ箱はまだありません。」と表示する。

## 動作確認

1. テスト用に `burnable`, `nonburnable`, `burnable,can` という3種類のレコードをDBに登録する。
2. `/list/burnable` にアクセスし、`burnable` と `burnable,can` の2件だけが表示され、`nonburnable` は含まれないことを確認する（部分一致の誤動作が起きていないことの確認）。
3. `/list/nonburnable`, `/list/can`, `/list/pet_bottle` でもそれぞれ正しく絞り込まれることを確認する。
4. 確認が終わったら、テスト用に登録したレコードはDBから削除しておく。
