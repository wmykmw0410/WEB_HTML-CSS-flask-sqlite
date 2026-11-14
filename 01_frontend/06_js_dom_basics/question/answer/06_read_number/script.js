// 解答6：文字を読み取って計算する

// TODO 1：textContent で読んだ値は文字列。Number() で数値にしてから計算する
const unitPrice = Number(document.getElementById('unit-price').textContent);
const quantity = Number(document.getElementById('quantity').textContent);
const total = unitPrice * quantity;
document.getElementById('total-output').textContent = `${total}円`;


// TODO 2：total は数値なので、+ は足し算になる（文字列のままだと '3000' + 500 → '3000500' になってしまう）
document.getElementById('shipping-output').textContent = `${total + 500}円`;


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

check('TODO 1：#total-output', text('total-output'), '3000円');
check('TODO 2：#shipping-output', text('shipping-output'), '3500円');
