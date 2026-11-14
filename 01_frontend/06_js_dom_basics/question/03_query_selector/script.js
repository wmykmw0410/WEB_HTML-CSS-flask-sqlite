// TODO 1：querySelector で <h1> を取得し、文字を「タグで取得しました」に書き換える


// TODO 2：querySelector で id が heading の要素を取得し、文字を「idで取得しました」に書き換える


// TODO 3：querySelector でクラスが note の要素を取得し、文字を「クラスで取得しました」に書き換える


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
