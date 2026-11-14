const form = document.getElementById('memo-form');
const titleInput = document.getElementById('title');
const titleError = document.getElementById('title-error');
const result = document.getElementById('result');

form.addEventListener('submit', (event) => {
    event.preventDefault();

    // TODO 1：タイトル（前後の空白を除いたもの）が空なら、titleError に「タイトルを入力してください」と表示し、
    //         result を空にして、処理を終わる（return）。
    //         問題が無ければ、titleError を空にして、result に「保存しました：（タイトル）」と表示する
});


// ============================================================
// テスト（ここから下は書き換えない）
// ============================================================
// ページの下の「テストを実行」ボタンを押すと、イベントが自動で起こされ、結果がConsoleに表示される
const check = (label, actual, expected) => {
    const ok = JSON.stringify(actual) === JSON.stringify(expected);
    if (ok) {
        console.log(`✅ ${label}`);
    } else {
        console.log(`❌ ${label}　結果：${JSON.stringify(actual)}　期待：${JSON.stringify(expected)}`);
    }
};

// id から、要素の文字を取り出す（要素が無いときは目印の文字を返す）
const text = (id) => {
    const el = document.getElementById(id);
    return el ? el.textContent : '（その id の要素が無い）';
};

// イベントを自動で起こす（click・keydown・submit など）
const fire = (target, type, init = {}) => {
    const noBubble = ['mouseenter', 'mouseleave', 'focus', 'blur'].includes(type);
    const options = { bubbles: !noBubble, cancelable: true, ...init };
    let event;
    if (type === 'keydown') {
        event = new KeyboardEvent(type, options);
    } else if (type === 'click' || type.startsWith('mouse')) {
        event = new MouseEvent(type, options);
    } else {
        event = new Event(type, options);
    }
    target.dispatchEvent(event);
    return event;
};

const runTests = () => {
    const form = document.getElementById('memo-form');
    const titleInput = document.getElementById('title');
    titleInput.value = '';
    fire(form, 'submit');
    check('TODO 1：空 → エラー', text('title-error'), 'タイトルを入力してください');
    check('TODO 1：空 → result は空', text('result'), '');
    titleInput.value = '   ';
    fire(form, 'submit');
    check('TODO 1：空白だけ → エラー', text('title-error'), 'タイトルを入力してください');
    titleInput.value = ' 会議 ';
    fire(form, 'submit');
    check('TODO 1：正しい入力 → エラーが消える', text('title-error'), '');
    check('TODO 1：正しい入力 → 保存しました（空白は除く）', text('result'), '保存しました：会議');
};

const testButton = document.createElement('button');
testButton.type = 'button';
testButton.textContent = 'テストを実行（結果はConsoleに表示）';
document.body.append(testButton);
testButton.addEventListener('click', runTests);
if (location.search.includes('autorun')) {
    runTests();
}
