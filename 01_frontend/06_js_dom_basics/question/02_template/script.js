const userName = '山田';
const price = 450;
const quantity = 3;
const memos = ['買い物リスト', '企画会議メモ', '読書メモ'];


// TODO 1：#name-output に「山田さん」と表示する（userName の値を埋め込む）


// TODO 2：#total-output に「1350円」と表示する（price と quantity から計算して埋め込む）


// TODO 3：#count-output に「3件」と表示する（memos の件数を埋め込む）


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

check('TODO 1：#name-output', text('name-output'), '山田さん');
check('TODO 2：#total-output', text('total-output'), '1350円');
check('TODO 3：#count-output', text('count-output'), '3件');
