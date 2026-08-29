# 登録フォームのテキスト配置を中央寄せ

日付: 2026-08-29

## これは何をする作業か

登録フォームが画面の左端に張り付いていて見た目が良くなかったため、フォーム全体をページ中央に配置する。

## 手順

1. `trash_map/static/form.css` を開き、フォームを囲む枠のスタイルを追加する。
   ```css
   .add-form-wrapper {
       max-width: 480px;
       margin: 40px auto;
       padding: 0 16px;
   }
   ```
   `margin: 40px auto;` の `auto` が左右の余白を自動計算し、結果として要素が中央に寄る。見出し（`<h1>`）も中央揃えにするスタイルを合わせて追加する。
2. `trash_map/templates/trash/add.html` を開き、`<h1>`から`</form>`までを `<div class="add-form-wrapper">...</div>` で囲む。

## 動作確認

- `/add` にアクセスし、フォームが画面の中央に表示されることを確認する。
