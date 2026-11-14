// TODO 1：canEdit(isLoggedIn, isAdmin)：ログイン中「かつ」管理者のときだけ true を返す（&&）
const canEdit = (isLoggedIn, isAdmin) => {
};


// TODO 2：hasInput(title, body)：タイトル「または」本文のどちらかが、空文字でなければ true を返す（||）
const hasInput = (title, body) => {
};


// TODO 3：isGuest(isLoggedIn)：ログインしていないとき true を返す（!）
const isGuest = (isLoggedIn) => {
};


// TODO 4：statusLabel(isDone)：isDone が true なら '完了'、false なら '未完了' を返す（三項演算子 条件 ? A : B）
const statusLabel = (isDone) => {
};


// TODO 5：titleMessage(title)：title が空文字なら 'タイトルを入力してください'、そうでなければ空文字 '' を返す（三項演算子）
const titleMessage = (title) => {
};


// ============================================================
// テスト（ここから下は書き換えない）
// ============================================================
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

const get = (fn) => {
    try {
        return fn();
    } catch (error) {
        return '（未定義・エラー）';
    }
};

check('TODO 1：canEdit(true, true)', get(() => canEdit(true, true)), true);
check('TODO 1：canEdit(true, false)', get(() => canEdit(true, false)), false);
check('TODO 1：canEdit(false, true)', get(() => canEdit(false, true)), false);
check('TODO 2：hasInput(\'\', \'\')', get(() => hasInput('', '')), false);
check('TODO 2：hasInput(\'a\', \'\')', get(() => hasInput('a', '')), true);
check('TODO 2：hasInput(\'\', \'b\')', get(() => hasInput('', 'b')), true);
check('TODO 3：isGuest(false)', get(() => isGuest(false)), true);
check('TODO 3：isGuest(true)', get(() => isGuest(true)), false);
check('TODO 4：statusLabel(true)', get(() => statusLabel(true)), '完了');
check('TODO 4：statusLabel(false)', get(() => statusLabel(false)), '未完了');
check('TODO 5：titleMessage(\'\')', get(() => titleMessage('')), 'タイトルを入力してください');
check('TODO 5：titleMessage(\'会議\')', get(() => titleMessage('会議')), '');