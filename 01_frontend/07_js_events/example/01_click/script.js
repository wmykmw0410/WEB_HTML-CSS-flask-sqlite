// ============================================================
// 1. ボタンを押すと文字が変わる
// ============================================================
// ① 動かしたい要素を、id で取得する
const helloButton = document.getElementById('hello-button');
const message = document.getElementById('message');

let count = 0;

// ② 「クリックされたら、この関数を呼んでね」と登録する（コールバック関数）
helloButton.addEventListener('click', () => {
    count++;
    // ③ textContent を書き換えると、画面の文字がすぐ変わる
    message.textContent = `${count}回押されました`;
});


// ============================================================
// 2. ボタンを押すたびに見た目が切り替わる
// ============================================================
const toggleButton = document.getElementById('toggle-button');
const toggleTarget = document.getElementById('toggle-target');

toggleButton.addEventListener('click', () => {
    // classList.toggle：クラスが無ければ付け、あれば外す（CSSの .highlight が当たる）
    toggleTarget.classList.toggle('highlight');
});
