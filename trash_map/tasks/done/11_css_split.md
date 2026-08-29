# インラインCSSを外部ファイルに分離

日付: 2026-08-29

## これは何をする作業か

HTMLファイルの `<style>` タグの中に直接書かれていたCSSを、`static/` 配下の別ファイルに切り出す。

## 手順

1. `map.html` の `<style>` の中身（`#map { height: calc(100vh - 48px); }`）を、以前から存在していたが実は誰からも読み込まれていなかった `static/trash.css`（Leafletマーカーの色を変えるCSSが入っていたファイル）に統合する。
2. `map.html` から `<style>` タグを削除し、代わりに `<link rel="stylesheet">` タグで `trash.css` を読み込むようにする。
   ```html
   <link rel="stylesheet" href="{{ url_for('static', filename='trash.css') }}">
   ```
3. `type_list.html` に書かれていた `.trash-list` / `.trash-card` などのCSSを、新規作成した `static/type_list.css` に切り出し、同様に `<link rel="stylesheet">` で読み込む形に変更する。

## 動作確認

1. `/static/trash.css`, `/static/type_list.css` にアクセスし、それぞれ `200` で正しい内容が返ることを確認する。
2. `/map`, `/list/burnable` のHTMLソースに `<style>` タグ（インラインCSS）が残っていないこと、外部CSSへの `<link>` が出力されていることを確認する。
