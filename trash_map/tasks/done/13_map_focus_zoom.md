# 詳細ページから該当ピンにズームして地図表示

日付: 2026-08-29

## これは何をする作業か

詳細ページから地図に戻ったとき、ただの地図全体表示ではなく、そのゴミ箱のピンの位置までズームインして表示されるようにする。

## 手順

1. `trash_map/templates/trash/detail.html` の「地図に戻る」リンクを「地図で見る」に変更し、リンク先にクエリパラメータ `focus` を付ける。
   ```html
   <a href="{{ url_for('index_page', focus=item.id) }}">地図で見る</a>
   ```
   これで、例えば `/?focus=1` のようなURLで地図ページに遷移するようになる。
2. `trash_map/templates/map/map.html` の `#map` に、URLのクエリパラメータをJavaScript側へ渡すための `data-focus-id` 属性を追加する。
   ```html
   <div id="map" data-api-url="..." data-focus-id="{{ request.args.get('focus', '') }}"></div>
   ```
3. `trash_map/static/js/map.js` で、マーカーを1つずつ作るループの中に、フォーカス対象かどうかの判定を追加する。
   ```javascript
   if (focusId && String(item.id) === focusId) {
       map.setView([item.latitude, item.longitude], 17);
       marker.openTooltip();
   }
   ```
   `data-*` 属性の値は常に文字列になるため、`item.id`（数値）を `String()` で文字列に変換してから比較している点に注意する。

## 動作確認

- `/trash/1` から「地図で見る」をクリックし、`/?focus=1` に遷移した上で、地図がそのゴミ箱の位置にズームインし、名前のツールチップが自動的に開くことを確認する。
