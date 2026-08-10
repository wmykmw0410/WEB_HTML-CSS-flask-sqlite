/*
練習問題：メモ帳アプリにJavaScriptで3つの機能を追加しよう

018_ownership_crudで作ったメモ帳アプリの見た目や機能はそのままです。
このファイルにJavaScriptを書いて、ページを再読み込みしない操作を追加します。

このファイルは全ページで読み込まれるため、対象の要素がそのページに
無いこともあります。`if (要素)` で存在チェックしてから使うようにしてください。
*/

// ============================================================
// 問題1：文字数カウンター（メモ追加・編集ページ）
// #body（本文のtextarea）に入力するたびに、#body-count（文字数表示）を更新する
// 500文字を超えたら #body-count に "over" クラスを付ける（CSSで赤字になる）
//
// ヒント：
//   const textarea = document.getElementById('body');
//   const counter = document.getElementById('body-count');
//   textarea.addEventListener('input', () => { ... });
//   counter.textContent = textarea.value.length;
//   counter.classList.toggle('over', textarea.value.length > 500);
// ============================================================
const bodyTextarea = document.getElementById('body');
if (bodyTextarea) {
    // TODO: 文字数カウンターを実装する
}


// ============================================================
// 問題2：カテゴリの絞り込み（メモ一覧ページ）
// .filters 内のボタンをクリックしたら、選択中のボタンにだけ active クラスを付け、
// .card-grid 内のカードのうち、data-category が一致しないものに hidden クラスを付ける
// （data-category="all" のボタンがクリックされたら全件表示する）
//
// ヒント：
//   const buttons = document.querySelectorAll('.filters button');
//   const cards = document.querySelectorAll('.card');
//   button.dataset.category / card.dataset.category で data-category 属性の値を取得できる
// ============================================================
const filterButtons = document.querySelectorAll('.filters button');
if (filterButtons.length > 0) {
    // TODO: カテゴリ絞り込みを実装する
}


// ============================================================
// 問題3：ピン留めをfetch()でトグルする（メモ一覧ページ）
// .pin-button をクリックしたら、そのメモの /memos/<id>/toggle-pin に
// fetch() でPOSTリクエストを送り、返ってきたJSONの is_pinned に応じて
// ボタンの表示（★ or ☆）を書き換える（ページの再読み込みはしない）
//
// 注意：このアプリはCSRFProtect(app)が有効なので、POSTには
// CSRFトークンが必要です。<meta name="csrf-token"> にすでに埋め込んで
// あるので、fetch() のheadersで 'X-CSRFToken' として送ってください。
//
// ヒント：
//   button.dataset.id でカードのdata-id属性（メモID）を取得できる
//   const token = document.querySelector('meta[name="csrf-token"]').content;
//   const response = await fetch(`/memos/${memoId}/toggle-pin`, {
//       method: 'POST',
//       headers: { 'X-CSRFToken': token },
//   });
//   const data = await response.json();
//   button.textContent = data.is_pinned ? '★' : '☆';
//   イベントリスナーの中で await を使うには、コールバック関数に async を付ける
//   例: button.addEventListener('click', async () => { ... });
// ============================================================
const pinButtons = document.querySelectorAll('.pin-button');
if (pinButtons.length > 0) {
    // TODO: ピン留めのトグルを実装する
}
