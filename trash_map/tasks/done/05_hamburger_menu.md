# ハンバーガーメニューでゴミ種別ごとの一覧に遷移できるように

日付: 2026-08-29

## これは何をする作業か

ヘッダーに「☰」のハンバーガーボタンを追加し、クリックするとゴミ種別（燃えるゴミ・不燃ごみ・缶・ペットボトル・瓶）ごとの一覧ページへのリンクが出るメニューを表示できるようにする。

## 手順

1. `trash_map/constants.py` を新規作成し、ゴミ種別の一覧を1箇所にまとめる（あちこちに同じリストを書かないため）。
   ```python
   GARBAGE_TYPES = [
       ("burnable", "燃えるゴミ"),
       ("nonburnable", "不燃ごみ"),
       ("can", "缶"),
       ("pet_bottle", "ペットボトル"),
       ("glass", "瓶"),
   ]
   ```
2. `trash_map/form.py` の `SelectMultipleField(choices=...)` に直接書いていたリストを、`from constants import GARBAGE_TYPES` で読み込んだこの定数に置き換える（同じ内容を2箇所に書かないようにするため）。
3. `trash_map/app.py` に、どのテンプレートからでもゴミ種別一覧を使えるようにする仕組み（`context_processor`）を追加する。
   ```python
   @app.context_processor
   def inject_garbage_types():
       return {"garbage_types": GARBAGE_TYPES}
   ```
4. 同じく `trash_map/app.py` に、種別ごとの一覧ページのルートを追加する（この時点ではまだDBと連携せず、「準備中です」と表示するだけの仮実装）。
   ```python
   @app.route("/list/<type_key>")
   def type_list_page(type_key):
       label = GARBAGE_TYPE_LABELS.get(type_key, type_key)
       return render_template("trash/type_list.html", label=label)
   ```
5. `trash_map/templates/base.html` のヘッダーに、3本線のハンバーガーボタンとメニュー（`<nav class="hamburger-menu">`）を追加する。メニューの中身は `{% for key, label in garbage_types %}` で `garbage_types` をループし、`url_for('type_list_page', type_key=key)` へのリンクを5件生成する。
6. ボタンの開閉やメニュー外クリックで閉じる動きはJavaScriptで実装する（クリックで `hidden` 属性を切り替える、`aria-expanded` 属性でアクセシビリティに配慮する）。
7. `trash_map/templates/map/map.html` にあった、未実装の `/burnable` へ飛ぶだけの暫定リンク「燃えるゴミ」（`.test-trashcan`）は、役割がハンバーガーメニューに統合されたので削除する。

## 動作確認

1. `/list/burnable`, `/list/nonburnable`, `/list/can`, `/list/pet_bottle`, `/list/glass` にアクセスし、すべて `200` が返ることを確認する。
2. 存在しない種別キー（例: `/list/unknown`）でも `200` が返ることを確認する（`GARBAGE_TYPE_LABELS.get(type_key, type_key)` により、未知のキーはそのまま表示されるだけでエラーにならない）。
3. `/map` を開き、ハンバーガーメニューに5種類分のリンクが正しいURL・日本語ラベルで出力されていることを確認する。
