const helloButton = document.getElementById('hello-button');
const message = document.getElementById('message');


// TODO 1：helloButton がクリックされたら、message の文字を「押されました」に書き換える


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
    check('押す前は、文字が変わらない', text('message'), 'まだ押されていません');
    fire(document.getElementById('hello-button'), 'click');
    check('TODO 1：クリックしたあと', text('message'), '押されました');
};

const testButton = document.createElement('button');
testButton.type = 'button';
testButton.textContent = 'テストを実行（結果はConsoleに表示）';
document.body.append(testButton);
testButton.addEventListener('click', runTests);
if (location.search.includes('autorun')) {
    runTests();
}
