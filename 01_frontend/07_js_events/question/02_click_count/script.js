const countButton = document.getElementById('count-button');
const countOutput = document.getElementById('count-output');


// TODO 1：回数を入れる変数 count を、0 から始めて用意する


// TODO 2：countButton がクリックされるたびに count を 1 増やし、countOutput に「1回押されました」「2回押されました」…と表示する


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
    const button = document.getElementById('count-button');
    check('押す前は、文字が変わらない', text('count-output'), 'まだ押されていません');
    fire(button, 'click');
    check('TODO 2：1回目', text('count-output'), '1回押されました');
    fire(button, 'click');
    check('TODO 2：2回目', text('count-output'), '2回押されました');
    fire(button, 'click');
    check('TODO 2：3回目', text('count-output'), '3回押されました');
};

const testButton = document.createElement('button');
testButton.type = 'button';
testButton.textContent = 'テストを実行（結果はConsoleに表示）';
document.body.append(testButton);
testButton.addEventListener('click', runTests);
if (location.search.includes('autorun')) {
    runTests();
}
