// 解答5：親要素でまとめてイベントを受け取る

const list = document.getElementById('memo-list');
const clickOutput = document.getElementById('click-output');


// TODO 1：event.target は、実際にクリックされた要素（li の中の span の場合もある）。
//         closest('li') で、自分または祖先から、最も近い li が手に入る（見つからなければ null）
list.addEventListener('click', (event) => {
    const item = event.target.closest('li');
    if (!item) {
        return;   // li の外がクリックされたときは、何もしない
    }
    clickOutput.textContent = `${item.dataset.category}のメモがクリックされました`;
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
    const list = document.getElementById('memo-list');
    const items = list.querySelectorAll('li');
    fire(items[0], 'click');
    check('TODO 1：li をクリック', text('click-output'), '家事のメモがクリックされました');
    fire(items[1].querySelector('.tag'), 'click');
    check('TODO 1：li の中のバッジをクリックしても、li が手に入る', text('click-output'), '仕事のメモがクリックされました');
    fire(list, 'click');
    check('TODO 1：li の外（ul 自身）をクリックしても、何も変わらない', text('click-output'), '仕事のメモがクリックされました');
};

const testButton = document.createElement('button');
testButton.type = 'button';
testButton.textContent = 'テストを実行（結果はConsoleに表示）';
document.body.append(testButton);
testButton.addEventListener('click', runTests);
if (location.search.includes('autorun')) {
    runTests();
}
