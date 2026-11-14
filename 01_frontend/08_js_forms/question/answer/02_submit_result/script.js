// 解答2：送信を止めて、結果を表示する

const form = document.getElementById('memo-form');
const titleInput = document.getElementById('title');
const result = document.getElementById('result');

form.addEventListener('submit', (event) => {
    event.preventDefault();

    // TODO 1：入力欄の値は .value。テンプレートリテラルで埋め込む
    result.textContent = `送信されました：${titleInput.value}`;
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
    const titleInput = document.getElementById('title');
    titleInput.value = '会議';
    fire(document.getElementById('memo-form'), 'submit');
    check('TODO 1：「会議」を送信', text('result'), '送信されました：会議');
    titleInput.value = '買い物';
    fire(document.getElementById('memo-form'), 'submit');
    check('TODO 1：「買い物」を送信', text('result'), '送信されました：買い物');
};

const testButton = document.createElement('button');
testButton.type = 'button';
testButton.textContent = 'テストを実行（結果はConsoleに表示）';
document.body.append(testButton);
testButton.addEventListener('click', runTests);
if (location.search.includes('autorun')) {
    runTests();
}
