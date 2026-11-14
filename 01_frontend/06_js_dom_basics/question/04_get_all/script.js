// TODO 1：クラスが item の要素をすべて取得し、その数を #count-output に「3個」と表示する


// TODO 2：タグが li の要素をすべて取得し、その数を #tag-count-output に「3個」と表示する


// TODO 3：クラスが name の要素をすべて取得し、最初の商品名を #first-output に表示する


// TODO 4：（TODO 3 で取得したものを使って）最後の商品名を #last-output に表示する


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

check('TODO 1：#count-output', text('count-output'), '3個');
check('TODO 2：#tag-count-output', text('tag-count-output'), '3個');
check('TODO 3：#first-output', text('first-output'), 'りんご');
check('TODO 4：#last-output', text('last-output'), 'みかん');
