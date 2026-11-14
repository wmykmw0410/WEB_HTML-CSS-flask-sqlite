// 解答7：条件を組み合わせる・三項演算子（発展）

// TODO 1：A && B は、両方が true のときだけ true
const canEdit = (isLoggedIn, isAdmin) => {
    return isLoggedIn && isAdmin;
};


// TODO 2：A || B は、どちらかが true なら true
const hasInput = (title, body) => {
    return title !== '' || body !== '';
};


// TODO 3：!A は、true と false を入れ替える
const isGuest = (isLoggedIn) => {
    return !isLoggedIn;
};


// TODO 4：条件 ? 真のとき : 偽のとき（条件が先。Python の「値 if 条件 else 値」とは順番が逆）
const statusLabel = (isDone) => {
    return isDone ? '完了' : '未完了';
};


// TODO 5：if / else で値を選ぶ処理を、1行で書ける
const titleMessage = (title) => {
    return title === '' ? 'タイトルを入力してください' : '';
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