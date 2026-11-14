// 解答1：属性を読み書きする

// TODO 1：querySelector は CSS のセレクタで要素を1つ取得する。setAttribute('属性名', '値')
const link = document.querySelector('a.doc-link');
link.setAttribute('target', '_blank');
link.setAttribute('rel', 'noopener noreferrer');   // target="_blank" とセットで付ける


// TODO 2：getAttribute('属性名') で、属性の値を読む
document.getElementById('href-output').textContent = link.getAttribute('href');


// TODO 3：data-lang="ja" は dataset.lang で読める（ハイフンはキャメルケースになる）
document.getElementById('lang-output').textContent = `言語：${link.dataset.lang}`;


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
    const link = document.querySelector('a.doc-link');
    check('TODO 1：target', link.getAttribute('target'), '_blank');
    check('TODO 1：rel', link.getAttribute('rel'), 'noopener noreferrer');
    check('TODO 2：#href-output', text('href-output'), 'https://developer.mozilla.org/ja/');
    check('TODO 3：#lang-output', text('lang-output'), '言語：ja');
};

const testButton = document.createElement('button');
testButton.type = 'button';
testButton.textContent = 'テストを実行（結果はConsoleに表示）';
document.body.append(testButton);
testButton.addEventListener('click', runTests);
if (location.search.includes('autorun')) {
    runTests();
}
