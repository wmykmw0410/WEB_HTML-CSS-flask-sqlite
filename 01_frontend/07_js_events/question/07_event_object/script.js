const eventButton = document.getElementById('event-button');
const typeOutput = document.getElementById('type-output');
const keyInput = document.getElementById('key-input');
const keyOutput = document.getElementById('key-output');


// TODO 1：eventButton がクリックされたら、イベントの種類（event.type）を typeOutput に表示する


// TODO 2：keyInput でキーが押されたら（keydown）、「押されたキー：a」のように、押されたキー（event.key）を keyOutput に表示する


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
    fire(document.getElementById('event-button'), 'click');
    check('TODO 1：event.type', text('type-output'), 'click');
    const keyInput = document.getElementById('key-input');
    fire(keyInput, 'keydown', { key: 'a' });
    check('TODO 2：a キー', text('key-output'), '押されたキー：a');
    fire(keyInput, 'keydown', { key: 'Enter' });
    check('TODO 2：Enter キー', text('key-output'), '押されたキー：Enter');
};

const testButton = document.createElement('button');
testButton.type = 'button';
testButton.textContent = 'テストを実行（結果はConsoleに表示）';
document.body.append(testButton);
testButton.addEventListener('click', runTests);
if (location.search.includes('autorun')) {
    runTests();
}
