// 解答6：textContentとinnerHTML

// ユーザーが入力した文字だと思ってください（タグを含んでいる）
const userInput = `<img src=x onerror="alert('乗っ取り')">`;


// TODO 1：ユーザーの入力は textContent で入れる（innerHTML だとタグとして解釈され、XSS の原因になる）
document.getElementById('user-output').textContent = userInput;


// TODO 2：自分で書いた固定のHTMLなら、innerHTML で入れてよい（ユーザーの入力を混ぜない）
document.getElementById('trusted-output').innerHTML = '<b>太字</b>の文字';


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
    const userInput = `<img src=x onerror="alert('乗っ取り')">`;
    check('TODO 1：タグが文字として表示される', text('user-output'), userInput);
    check('TODO 1：img 要素が作られていない', document.querySelectorAll('#user-output img').length, 0);
    check('TODO 2：b 要素になっている', document.querySelectorAll('#trusted-output b').length, 1);
    check('TODO 2：文字', text('trusted-output'), '太字の文字');
};

const testButton = document.createElement('button');
testButton.type = 'button';
testButton.textContent = 'テストを実行（結果はConsoleに表示）';
document.body.append(testButton);
testButton.addEventListener('click', runTests);
if (location.search.includes('autorun')) {
    runTests();
}
