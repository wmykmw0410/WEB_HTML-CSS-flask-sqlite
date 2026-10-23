/*
    制作課題ステップ3：全ページ共通のスクリプト（js/script.js）

    HTML と CSS は完成しています（☰ ボタン・絞り込みボタン・エラー表示用の <p> などを追加済み）。
    TODO を埋めて、3つの動きを付けてください。完成例は answer/js/script.js にあります。

    このファイルは全ページで読み込まれるので、ページによっては対象の要素がありません。
    if (要素) で存在を確認してから使います（05_js_basics の1節「真偽の判定」）。
*/

// ============================================================
// TODO 1（06_js_events 1節・07_js_dom 1節）：ハンバーガーメニュー（全ページ）
// #nav-toggle をクリックするたびに #nav-links の open クラスを付け外しし、
// ボタンの open クラスを付け外しする
// ヒント：classList.toggle('open') は、付けたら true・外したら false を返す
// ============================================================
const navToggle = document.getElementById('nav-toggle');
if (navToggle) {
    // TODO
}


// ============================================================
// TODO 2（08_js_render 1節・この章の3節）：制作実績の絞り込み（works.html）
// #filters の中のボタンがクリックされたら（親の #filters に1回だけイベントを登録する）、
// - 押されたボタンだけに active クラスを付ける
// - 各 .work-card の data-tags（"HTML/CSS JavaScript" のような空白区切り）を split(' ') で配列にし、
//   選ばれたタグ（button.dataset.tag）を includes() で含まないカードに hidden クラスを付ける
//   （data-tag="all" のボタンなら全件表示）
// ヒント：押されたボタンは event.target.closest('button') で取得する
// ============================================================
const filters = document.getElementById('filters');
if (filters) {
    // TODO
}


// ============================================================
// TODO 3（06_js_events 3節）：お問い合わせフォームの入力チェック（contact.html）
// フォームの submit で次をチェックし、問題があれば各欄の下の <p class="error" id="（入力欄のid）-error"> に
// メッセージを表示して、入力欄に invalid クラスを付ける（問題が無い欄はメッセージを消してクラスを外す）
//   - お名前：空（空白だけ）なら「お名前を入力してください」
//   - メールアドレス：@ を含まなければ「メールアドレスの形式で入力してください」
//   - メッセージ：空白を除いて10文字未満なら「メッセージは10文字以上で入力してください」
// すべて問題なければ #contact-result に「（お名前）さん、お問い合わせありがとうございました。」と表示し、フォームを reset() する
// このサイトは静的なページで送信先のサーバーが無いので、送信自体は必ず event.preventDefault() で止める
// ============================================================
const contactForm = document.getElementById('contact-form');
if (contactForm) {
    // TODO
}
