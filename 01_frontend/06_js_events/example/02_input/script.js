// ============================================================
// 入力に反応する（文字数カウンター）
// ============================================================
// 1. 要素を取得する
const textarea = document.getElementById('body');
const counter = document.getElementById('count');

// 2. 'input' イベント：入力欄の中身が変わるたびに（1文字ごとに）呼ばれる
textarea.addEventListener('input', () => {
    const length = textarea.value.length;   // 入力欄の中身は .value で取得する

    // 3. textContent を書き換えると画面表示が更新される
    counter.textContent = length;

    // 4. classList.toggle() で条件に応じてCSSクラスを付け外しする
    counter.classList.toggle('over', length > 450);
});
