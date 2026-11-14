// 解答1：取得して書き換える

// TODO 1：① 取得 → ② 書き換え。id は # を付けずに書く
const title = document.getElementById('title');
title.textContent = 'はじめてのDOM';


// TODO 2：どの要素でも、同じ2ステップ
const message = document.getElementById('message');
message.textContent = 'JavaScriptで書き換えました';


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
