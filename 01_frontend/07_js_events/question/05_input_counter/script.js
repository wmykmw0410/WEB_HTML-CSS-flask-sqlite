const textarea = document.getElementById('body');
const counter = document.getElementById('count');


// TODO 1：textarea に入力されるたびに、入力された文字数を counter に表示する


// TODO 2：文字数が 10 を超えたら、counter に over クラスを付ける（10 以下に戻ったら外す）
//         （CSS の .over で、赤字になる）


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
    const textarea = document.getElementById('body');
    const counter = document.getElementById('count');
    textarea.value = 'abc';
    fire(textarea, 'input');
    check('TODO 1：3文字', text('count'), '3');
    check('TODO 2：3文字のとき、over が付いていない', counter.classList.contains('over'), false);
    textarea.value = 'abcdefghijk';
    fire(textarea, 'input');
    check('TODO 1：11文字', text('count'), '11');
    check('TODO 2：11文字のとき、over が付いている', counter.classList.contains('over'), true);
    textarea.value = 'abcdefghij';
    fire(textarea, 'input');
    check('TODO 2：10文字に戻すと、over が外れる', counter.classList.contains('over'), false);
};

const testButton = document.createElement('button');
testButton.type = 'button';
testButton.textContent = 'テストを実行（結果はConsoleに表示）';
document.body.append(testButton);
testButton.addEventListener('click', runTests);
if (location.search.includes('autorun')) {
    runTests();
}
