// TODO 1：#title の要素を取得して、文字を「はじめてのDOM」に書き換える


// TODO 2：#message の要素を取得して、文字を「JavaScriptで書き換えました」に書き換える


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

check('TODO 1：#title', text('title'), 'はじめてのDOM');
check('TODO 2：#message', text('message'), 'JavaScriptで書き換えました');
