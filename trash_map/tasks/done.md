# 作業記録（インデックス）

機能ごとに `tasks/done/` 配下のファイルへ分割しました。各ファイルは「これは何をする作業か」→「手順（番号付き）」→「動作確認」という手順書の形式で書かれており、同じ変更を後から自分の手で再現・理解できるようになっています。

## リファレンス

- [00_function_reference.md](done/00_function_reference.md) — 主な関数・クラスの役割の解説（手順書ではなく、コードを読むための参考資料）

## 作業手順（実施順）

- [01_templates_reorg.md](done/01_templates_reorg.md) — `templates/` を機能別フォルダ（map/trash/error/draft）に再構成
- [02_garbage_type_multiselect.md](done/02_garbage_type_multiselect.md) — ゴミの種類をチェックボックスで複数選択できるように変更
- [03_common_header.md](done/03_common_header.md) — 全ページ共通ヘッダー（`base.html`）を追加
- [04_form_centering.md](done/04_form_centering.md) — 登録フォームをページ中央に配置
- [05_hamburger_menu.md](done/05_hamburger_menu.md) — ハンバーガーメニューでゴミ種別ごとの一覧に遷移
- [06_type_list_db_integration.md](done/06_type_list_db_integration.md) — ゴミ種別ごとの一覧ページをDBと連携
- [07_postal_code_and_photo.md](done/07_postal_code_and_photo.md) — 郵便番号・写真の登録機能を追加
- [08_sample_data.md](done/08_sample_data.md) — サンプルデータの登録・カード表示への調整
- [09_map_pin_to_detail.md](done/09_map_pin_to_detail.md) — 地図のピンをクリックしたら詳細ページに遷移
- [10_js_split.md](done/10_js_split.md) — インラインJSを `static/js/*.js` に分離
- [11_css_split.md](done/11_css_split.md) — インラインCSSを `static/*.css` に分離
- [12_update_date_and_edit_page.md](done/12_update_date_and_edit_page.md) — 更新日カラムと編集ページを追加
- [13_map_focus_zoom.md](done/13_map_focus_zoom.md) — 詳細ページから該当ピンにズームして地図表示
- [14_nearby_search.md](done/14_nearby_search.md) — 現在地からの周辺検索機能を追加
- [15_address_split.md](done/15_address_split.md) — 住所を都道府県・市区町村・番地に分割、郵便番号自動補完
- [16_latlng_validation.md](done/16_latlng_validation.md) — 緯度・経度バリデーションの日本語化とプレースホルダー追加
- [17_qa_check.md](done/17_qa_check.md) — 全体QAチェック（一区切り）
- [18_formatting_and_comments.md](done/18_formatting_and_comments.md) — フォーマット修正・コメント追加

## 記録に残っていない細かい変更

チャット上でのやり取りのみで `done/` に記録を残さなかった小さな変更もあります（例: 未使用だった `templates/draft/` フォルダの削除、地図右下の「ゴミ箱を登録」ボタン削除、`type_list.html` のカードから詳細ページへのリンク化、`detail.html` のページ中央寄せ用CSS切り出しなど）。コードの現状は各ファイルの実装を直接確認してください。
