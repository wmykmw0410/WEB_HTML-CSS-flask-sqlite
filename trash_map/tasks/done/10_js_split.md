# インラインJSを外部ファイルに分離

日付: 2026-08-29

## これは何をする作業か

HTMLファイルの中に直接書かれていたJavaScriptを、`static/js/` 配下の別ファイルに切り出す。HTMLとJSを分けることで、それぞれ見通しが良くなる。

## 手順

1. `trash_map/static/js/header.js` を新規作成し、`base.html` に直接書かれていたハンバーガーメニューの開閉トグル処理をそのまま移す。この処理はDOM操作だけで、`fetch` や `{{ url_for(...) }}` のようなJinjaの変数を使っていないため、そのまま切り出すだけで済む。
2. `trash_map/static/js/map.js` を新規作成し、`map.html` に直接書かれていた「地図の初期化」「`/api/trashcans` の取得」「マーカー描画」「クリック時の遷移」の処理を移す。
   - 注意点: `{{ url_for('api_trashcans') }}` はJinjaのテンプレート内でしか解決できない（`.js`ファイルはFlaskのテンプレートエンジンを通らない）。そのため、URLをHTML側の `data-*` 属性経由でJSに渡す形に変更する。
     ```html
     <div id="map" data-api-url="{{ url_for('api_trashcans') }}"></div>
     ```
     ```javascript
     const apiUrl = document.getElementById('map').dataset.apiUrl;
     ```
3. `trash_map/templates/base.html` に `{% block scripts %}{% endblock %}` を追加する。これにより、各ページ（子テンプレート）が自分専用のスクリプト（leaflet本体や `map.js` など）をこのブロックに差し込めるようになる。
4. `map.html` の `<script>` タグを、外部ファイルを読み込む形に書き換える。
   ```html
   {% block scripts %}
   <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
   <script src="{{ url_for('static', filename='js/map.js') }}"></script>
   {% endblock %}
   ```

## 動作確認

1. `/static/js/header.js`, `/static/js/map.js` にアクセスし、それぞれ `200` で内容が返ることを確認する。
2. `/map` のHTMLソースにインラインの `fetch(...)` が残っていないこと、`data-api-url="/api/trashcans"` と外部スクリプトへの `<script src="...">` が正しく出力されていることを確認する。
