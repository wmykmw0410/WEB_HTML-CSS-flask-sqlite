// 解答4：入力した文字をそのまま表示する

const nameInput = document.getElementById('name-input');
const nameOutput = document.getElementById('name-output');


// TODO 1：クリックではなく 'input' イベント。入力欄の中身は .value
nameInput.addEventListener('input', () => {
    nameOutput.textContent = nameInput.value;
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
    const input = document.getElementById('name-input');
    input.value = '山田';
    fire(input, 'input');
    check('TODO 1：「山田」と入力', text('name-output'), '山田');
    input.value = '佐藤花子';
    fire(input, 'input');
    check('TODO 1：「佐藤花子」に変える', text('name-output'), '佐藤花子');
    input.value = '';
    fire(input, 'input');
    check('TODO 1：空にする', text('name-output'), '');
};

const testButton = document.createElement('button');
testButton.type = 'button';
testButton.textContent = 'テストを実行（結果はConsoleに表示）';
document.body.append(testButton);
testButton.addEventListener('click', runTests);
if (location.search.includes('autorun')) {
    runTests();
}
