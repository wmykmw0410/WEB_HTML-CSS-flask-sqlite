const form = document.getElementById('memo-form');
const titleInput = document.getElementById('title');
const bodyInput = document.getElementById('body');
const titleError = document.getElementById('title-error');
const bodyError = document.getElementById('body-error');
const result = document.getElementById('result');


// エラー表示を切り替える関数（練習問題5で書いたもの）
const showError = (input, errorEl, message) => {
    errorEl.textContent = message;
    input.classList.toggle('invalid', message !== '');
};


// TODO 1：フォームの submit で、タイトルと本文の両方をチェックする（showError を使う）
//         ・送信（ページの再読み込み）は、チェック結果にかかわらず止める
//         ・タイトルが、前後の空白を除いて空なら「タイトルを入力してください」
//         ・本文が、前後の空白を除いて10文字未満なら「本文は10文字以上で入力してください」
//         ・2つの欄は別々に調べる（片方がエラーでも、もう片方の表示は更新する）。問題が無い欄は、エラーを消す
//         ・どちらかにエラーがあれば、result を空にして処理を終わる。無ければ result に「保存しました：（タイトル）」と表示する


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
    const form = document.getElementById('memo-form');
    const titleInput = document.getElementById('title');
    const bodyInput = document.getElementById('body');
    titleInput.value = '';
    bodyInput.value = '';
    fire(form, 'submit');
    check('TODO 1：何も入力しない → タイトルのエラー', text('title-error'), 'タイトルを入力してください');
    check('TODO 1：何も入力しない → 本文のエラー', text('body-error'), '本文は10文字以上で入力してください');
    check('TODO 1：何も入力しない → 両方に invalid', titleInput.classList.contains('invalid') && bodyInput.classList.contains('invalid'), true);
    titleInput.value = '会議';
    fire(form, 'submit');
    check('TODO 1：タイトルだけ入力 → タイトルのエラーが消える', text('title-error'), '');
    check('TODO 1：タイトルだけ入力 → 本文のエラーは残る', text('body-error'), '本文は10文字以上で入力してください');
    check('TODO 1：タイトルだけ入力 → タイトルの invalid が外れる', titleInput.classList.contains('invalid'), false);
    bodyInput.value = '123456789';
    fire(form, 'submit');
    check('TODO 1：本文が9文字 → エラー', text('body-error'), '本文は10文字以上で入力してください');
    bodyInput.value = '  1234567890  ';
    fire(form, 'submit');
    check('TODO 1：本文が10文字 → エラーが消える', text('body-error'), '');
    check('TODO 1：すべて正しい → 保存しました', text('result'), '保存しました：会議');
};

const testButton = document.createElement('button');
testButton.type = 'button';
testButton.textContent = 'テストを実行（結果はConsoleに表示）';
document.body.append(testButton);
testButton.addEventListener('click', runTests);
if (location.search.includes('autorun')) {
    runTests();
}
