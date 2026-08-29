# 全ページ共通ヘッダーを追加

日付: 2026-08-29

## これは何をする作業か

各ページがそれぞれ独立した`<html>`〜`<body>`を持っていて、サイトタイトルやナビゲーションが無かった。全ページで共通のヘッダー（サイトタイトル＋ナビゲーション）を持つ土台となるテンプレートを作り、既存ページをそこに乗せ換える。

## 手順

1. `trash_map/templates/base.html` を新規作成する。中身は次の3つの部品でできている。
   - `<header class="site-header">` — サイトタイトル「ゴミ箱マップ」とナビゲーション（地図・登録へのリンク）。
   - `{% block title %}` — 各ページでタブのタイトルを差し替えられる場所。
   - `{% block head %}` — 各ページ固有のCSSなどを追加できる場所。
   - `{% block content %}` — 各ページの本文（`<body>`の中身）が入る場所。
   - ナビゲーションのリンク先は `url_for('index_page')` / `url_for('add_page')` のように、まだ実装されていないルートは含めず、既存のものだけにする。
2. 既存の各テンプレートを開き、`{% extends "base.html" %}` を先頭に追加して `base.html` を継承する形に書き換える。対象は `map/map.html`, `trash/add.html`, `trash/thankyou.html`, `trash/list.html`, `trash/detail.html`, `error/wrong.html`, `draft/home.html`, `draft/burnable.html` の全て（`trash/` はテンプレート内のサブフォルダ名で、プロジェクトルートの `trash_map/` とは別物）。
3. 各ファイルの `<!DOCTYPE html>`〜`<head>`〜`<body>` という共通の骨組みを削除し、ページ固有の`<head>`内容（CSS読み込みなど）は `{% block head %}...{% endblock %}` に、`<body>`の中身は `{% block content %}...{% endblock %}` に移す。
4. `map/map.html` にあった `body{margin:0}` などの共通スタイルは `base.html` 側に統合する。地図の高さはヘッダー分（48px）を差し引いて `calc(100vh - 48px)` に調整する。
5. ついでに、`trash/thankyou.html` と `error/wrong.html` にあった `<a href="/"></a>` のようなテキストなしリンク（クリックする場所が見た目上わからない不具合）を「地図に戻る」「登録ページに戻る」というテキスト付きリンクに直す。

## 動作確認

1. `/`, `/map`, `/add`, `/thankyou` にアクセスし、引き続き `200` が返ることを確認する。
2. まだルートが実装されていない `trash/list.html`, `trash/detail.html`, `error/wrong.html`, `draft/home.html`, `draft/burnable.html` も、`render_template()` を単体で呼び出してエラーが出ないこと、ヘッダーが表示されることを確認する。
