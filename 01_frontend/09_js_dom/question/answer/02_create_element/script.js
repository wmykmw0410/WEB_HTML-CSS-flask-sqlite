// 解答2：要素を1つ作って追加する

const list = document.getElementById('memo-list');


// TODO 1：createElement で作る（この時点では、まだ画面に無い）→ append で、画面上の要素に追加して、初めて表示される
const first = document.createElement('li');
first.textContent = '買い物リスト';
list.append(first);


// TODO 2：class は className で設定する
const second = document.createElement('li');
second.textContent = '企画会議メモ';
second.className = 'done';
list.append(second);


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
    const items = document.querySelectorAll('#memo-list li');
    check('TODO 1・2：li が2つ', items.length, 2);
    check('TODO 1：1つ目の文字', items[0] ? items[0].textContent : '', '買い物リスト');
    check('TODO 2：2つ目の文字', items[1] ? items[1].textContent : '', '企画会議メモ');
    check('TODO 2：2つ目の class', items[1] ? items[1].className : '', 'done');
};

const testButton = document.createElement('button');
testButton.type = 'button';
testButton.textContent = 'テストを実行（結果はConsoleに表示）';
document.body.append(testButton);
testButton.addEventListener('click', runTests);
if (location.search.includes('autorun')) {
    runTests();
}
