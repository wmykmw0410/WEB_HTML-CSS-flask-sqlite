// 解答2：変数や計算結果を表示する

const userName = '山田';
const price = 450;
const quantity = 3;
const memos = ['買い物リスト', '企画会議メモ', '読書メモ'];


// TODO 1：テンプレートリテラル（バッククォート）で、変数を埋め込む
document.getElementById('name-output').textContent = `${userName}さん`;


// TODO 2：計算は ${ } の中に書ける
document.getElementById('total-output').textContent = `${price * quantity}円`;


// TODO 3：配列の件数は length（() を付けない）
document.getElementById('count-output').textContent = `${memos.length}件`;


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
