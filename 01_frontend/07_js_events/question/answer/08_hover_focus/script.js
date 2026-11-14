// 解答8：ホバーとフォーカスで説明を出す

const tipButton = document.getElementById('tip-button');
const tip = document.getElementById('tip');


// TODO 1：mouseenter / mouseleave は、マウスが乗った / 外れたとき
tipButton.addEventListener('mouseenter', () => {
    tip.textContent = 'メモを新しく作ります';
});
tipButton.addEventListener('mouseleave', () => {
    tip.textContent = '';
});


// TODO 2：focus / blur は、キーボードで選ばれた / 外れたとき。マウスを使わない人にも同じ説明を届ける
tipButton.addEventListener('focus', () => {
    tip.textContent = 'メモを新しく作ります';
});
tipButton.addEventListener('blur', () => {
    tip.textContent = '';
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
    const tipButton = document.getElementById('tip-button');
    check('最初は、説明が出ていない', text('tip'), '');
    fire(tipButton, 'mouseenter');
    check('TODO 1：mouseenter', text('tip'), 'メモを新しく作ります');
    fire(tipButton, 'mouseleave');
    check('TODO 1：mouseleave', text('tip'), '');
    fire(tipButton, 'focus');
    check('TODO 2：focus', text('tip'), 'メモを新しく作ります');
    fire(tipButton, 'blur');
    check('TODO 2：blur', text('tip'), '');
};

const testButton = document.createElement('button');
testButton.type = 'button';
testButton.textContent = 'テストを実行（結果はConsoleに表示）';
document.body.append(testButton);
testButton.addEventListener('click', runTests);
if (location.search.includes('autorun')) {
    runTests();
}
