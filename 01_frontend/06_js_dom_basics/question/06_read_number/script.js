// TODO 1：#unit-price と #quantity の文字を読み取り、数値に変換して掛け算する。結果を #total-output に「3000円」と表示する


// TODO 2：TODO 1 の合計に、送料 500円 を足した金額を #shipping-output に「3500円」と表示する


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
