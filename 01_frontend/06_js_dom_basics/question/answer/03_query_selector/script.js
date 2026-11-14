// 解答3：querySelectorで1つ取得する

// TODO 1：タグ名は、そのまま書く
document.querySelector('h1').textContent = 'タグで取得しました';


// TODO 2：id は # を付ける（getElementById とは違い、# が必要）
document.querySelector('#heading').textContent = 'idで取得しました';


// TODO 3：クラスは . を付ける
document.querySelector('.note').textContent = 'クラスで取得しました';


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

check('TODO 1：h1', document.querySelector('h1').textContent, 'タグで取得しました');
check('TODO 2：#heading', document.querySelector('#heading').textContent, 'idで取得しました');
check('TODO 3：.note', document.querySelector('.note').textContent, 'クラスで取得しました');
