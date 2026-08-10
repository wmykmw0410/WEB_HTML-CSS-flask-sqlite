// 1. document.getElementById() で要素を取得する
const textarea = document.getElementById('body');
const counter = document.getElementById('count');

// 2. addEventListener() でイベント（入力のたびに発火する 'input'）を監視する
textarea.addEventListener('input', () => {
    const length = textarea.value.length;

    // 3. textContent を書き換えると画面表示が更新される
    counter.textContent = length;

    // 4. classList.toggle() で条件に応じてCSSクラスを付け外しする
    counter.classList.toggle('over', length > 450);
});
