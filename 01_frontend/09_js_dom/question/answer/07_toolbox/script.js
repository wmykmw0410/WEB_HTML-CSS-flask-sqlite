// 解答7：道具箱：classList・disabled・hidden・focus

const sendButton = document.getElementById('send-button');
const notice = document.getElementById('notice');
const box = document.getElementById('box');
const stateOutput = document.getElementById('state-output');
const nameInput = document.getElementById('name-input');


// TODO 1：disabled = true で押せなくなる（false で戻る）
sendButton.disabled = true;


// TODO 2：hidden = true で隠れる（false で表示）
notice.hidden = true;


// TODO 3：add は付ける、remove は外す（toggle と違い、条件に関係なく）
box.classList.add('active');
box.classList.remove('old');


// TODO 4：contains は、そのクラスが付いているかを true / false で返す
stateOutput.textContent = `active：${box.classList.contains('active')}`;


// TODO 5：focus() で、その要素にフォーカスを移す
nameInput.focus();


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
    check('TODO 1：disabled', document.getElementById('send-button').disabled, true);
    check('TODO 2：hidden', document.getElementById('notice').hidden, true);
    const box = document.getElementById('box');
    check('TODO 3：active が付いている', box.classList.contains('active'), true);
    check('TODO 3：old が外れている', box.classList.contains('old'), false);
    check('TODO 4：#state-output', text('state-output'), 'active：true');
    check('TODO 5：フォーカスが nameInput にある', document.activeElement === document.getElementById('name-input'), true);
};

const testButton = document.createElement('button');
testButton.type = 'button';
testButton.textContent = 'テストを実行（結果はConsoleに表示）';
document.body.append(testButton);
testButton.addEventListener('click', runTests);
if (location.search.includes('autorun')) {
    runTests();
}
