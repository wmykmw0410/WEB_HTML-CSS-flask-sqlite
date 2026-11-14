// 解答4：要素を消す

// TODO 1：消したい要素を取得して、remove() を呼ぶ
document.querySelector('#memo-list .old').remove();


// TODO 2：textContent に空文字を代入すると、子要素もすべて消える
document.getElementById('temp-list').textContent = '';


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
    const memoItems = document.querySelectorAll('#memo-list li');
    check('TODO 1：#memo-list の li の数', memoItems.length, 2);
    check('TODO 1：old の li が無い', document.querySelectorAll('#memo-list .old').length, 0);
    check('TODO 1：残った li', Array.from(memoItems).map((li) => li.textContent), ['買い物リスト', '企画会議メモ']);
    check('TODO 2：#temp-list の li の数', document.querySelectorAll('#temp-list li').length, 0);
};

const testButton = document.createElement('button');
testButton.type = 'button';
testButton.textContent = 'テストを実行（結果はConsoleに表示）';
document.body.append(testButton);
testButton.addEventListener('click', runTests);
if (location.search.includes('autorun')) {
    runTests();
}
