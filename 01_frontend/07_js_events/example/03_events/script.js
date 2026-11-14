// ============================================================
// 1. イベントオブジェクト
// ============================================================
// addEventListener のコールバック関数は、引数で「イベントオブジェクト」を受け取れる。
// 何が起きたか（どんなイベントか・どのキーが押されたか など）の情報が入っている
const eventButton = document.getElementById('event-button');
const clickOutput = document.getElementById('click-output');

eventButton.addEventListener('click', (event) => {
    // event.type：イベントの種類（'click' など）
    clickOutput.textContent = `${event.type} イベントが起きました`;
});

// キーボードのイベント
const keyInput = document.getElementById('key-input');
const keyOutput = document.getElementById('key-output');

keyInput.addEventListener('keydown', (event) => {
    // event.key：押されたキー（'a'、'Enter'、'Shift' など）
    keyOutput.textContent = `押されたキー：${event.key}`;
});


// ============================================================
// 2. ホバー（マウスを乗せる）とフォーカス
// ============================================================
// 見た目を変えるだけなら CSS の :hover で十分。
// 「別の要素に文字を出す」など、CSS だけではできないことを JavaScript で行う
const tipButton = document.getElementById('tip-button');
const tip = document.getElementById('tip');   // HTML 側では空にしてある（空のときは CSS の :empty で隠れる）

// mouseenter：マウスが要素に入ったとき ／ mouseleave：出たとき
tipButton.addEventListener('mouseenter', () => {
    tip.textContent = 'メモを新しく作ります';   // 文字を入れると表示される
});
tipButton.addEventListener('mouseleave', () => {
    tip.textContent = '';                      // 空にすると隠れる
});

// focus：Tab キーなどで要素が選ばれたとき ／ blur：選択が外れたとき
// マウスを使わない人にも同じ情報を届けるため、ホバーとセットで書く
tipButton.addEventListener('focus', () => {
    tip.textContent = 'メモを新しく作ります';
});
tipButton.addEventListener('blur', () => {
    tip.textContent = '';
});
