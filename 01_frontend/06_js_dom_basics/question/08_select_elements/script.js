// TODO 1：見出し（.page-title）を「商品一覧」にする


// TODO 2：商品（.item）の数を、#count-output に「3個」と表示する


// TODO 3：最初の商品名（.name の最初）を、#first-output に表示する


// TODO 4：すべての価格（.price）を足して、#sum-output に「350円」と表示する


// TODO 5：3つの価格の後ろに、それぞれ「円」を付ける（「120円」「80円」「150円」）


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

const texts = (selector) => Array.from(document.querySelectorAll(selector)).map((el) => el.textContent);
check('TODO 1：.page-title', document.querySelector('.page-title').textContent, '商品一覧');
check('TODO 2：#count-output', text('count-output'), '3個');
check('TODO 3：#first-output', text('first-output'), 'りんご');
check('TODO 4：#sum-output', text('sum-output'), '350円');
check('TODO 5：.price', texts('.price'), ['120円', '80円', '150円']);
