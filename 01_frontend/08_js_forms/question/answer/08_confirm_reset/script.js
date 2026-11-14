// 解答8：クリアの前に確認する（発展）

// 解答8：クリアの前に確認する（発展）

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


form.addEventListener('submit', (event) => {
    // このページには送信先が無いので、チェック結果にかかわらず送信は止める
    event.preventDefault();

    const title = titleInput.value.trim();
    const body = bodyInput.value.trim();

    // エラーがあったかどうかを、変数に覚えておく
    let hasError = false;

    if (title === '') {
        showError(titleInput, titleError, 'タイトルを入力してください');
        hasError = true;
    } else {
        showError(titleInput, titleError, '');
    }

    if (body.length < 10) {
        showError(bodyInput, bodyError, '本文は10文字以上で入力してください');
        hasError = true;
    } else {
        showError(bodyInput, bodyError, '');
    }

    if (hasError) {
        result.textContent = '';
        return;
    }

    result.textContent = `保存しました：${title}`;
});


// TODO 1・2：reset は「入力を消す」という既定の動作を持つイベント。preventDefault() で止められる
form.addEventListener('reset', (event) => {
    // 何か入力されているか（|| は「または」）
    const hasInput = titleInput.value !== '' || bodyInput.value !== '';

    // 入力があって、確認でキャンセルされたとき（&& は「かつ」、! は「でない」）
    if (hasInput && !confirm('入力内容を消しますか？')) {
        event.preventDefault();   // 入力を消す動作を止める
        return;
    }

    // TODO 2：消す場合は、エラー表示と結果も消す
    showError(titleInput, titleError, '');
    showError(bodyInput, bodyError, '');
    result.textContent = '';
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
    const form = document.getElementById('memo-form');
    const titleInput = document.getElementById('title');
    const bodyInput = document.getElementById('body');

    const originalConfirm = window.confirm;
    let asked = 0;
    const setConfirm = (answer) => {
        window.confirm = () => {
            asked++;
            return answer;
        };
    };

    // 入力して、送信して、エラーと結果を出しておく
    titleInput.value = '';
    bodyInput.value = 'abc';
    fire(form, 'submit');

    setConfirm(false);
    asked = 0;
    let event = fire(form, 'reset');
    check('TODO 1：入力あり・キャンセル → 入力を消さない（止める）', event.defaultPrevented, true);
    check('TODO 1：入力あり → 確認を出す', asked, 1);
    check('TODO 1：キャンセルのとき、エラー表示は消さない', text('body-error'), '本文は10文字以上で入力してください');

    setConfirm(true);
    asked = 0;
    event = fire(form, 'reset');
    check('TODO 1：入力あり・OK → 止めない', event.defaultPrevented, false);
    check('TODO 2：OK のとき、タイトルのエラーを消す', text('title-error'), '');
    check('TODO 2：OK のとき、本文のエラーを消す', text('body-error'), '');
    check('TODO 2：OK のとき、invalid クラスを外す', bodyInput.classList.contains('invalid'), false);
    check('TODO 2：OK のとき、result を空にする', text('result'), '');

    titleInput.value = '';
    bodyInput.value = '';
    setConfirm(false);
    asked = 0;
    event = fire(form, 'reset');
    check('TODO 1：入力なし → 確認を出さない', asked, 0);
    check('TODO 1：入力なし → 止めない', event.defaultPrevented, false);

    window.confirm = originalConfirm;
};

const testButton = document.createElement('button');
testButton.type = 'button';
testButton.textContent = 'テストを実行（結果はConsoleに表示）';
document.body.append(testButton);
testButton.addEventListener('click', runTests);
if (location.search.includes('autorun')) {
    runTests();
}
