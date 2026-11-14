// 解答4：複数の要素を取得して、数える・取り出す

// TODO 1：getElementsByClassName の結果は .length で数を調べられる（クラス名に . は付けない）
const items = document.getElementsByClassName('item');
document.getElementById('count-output').textContent = `${items.length}個`;


// TODO 2：getElementsByTagName も同じ
const lis = document.getElementsByTagName('li');
document.getElementById('tag-count-output').textContent = `${lis.length}個`;


// TODO 3：[0] で最初の要素を取り出す（番号は 0 から）
const names = document.getElementsByClassName('name');
document.getElementById('first-output').textContent = names[0].textContent;


// TODO 4：最後は、番号が「個数 - 1」（3個なら [2]）。この書き方なら、商品が増えても最後が取れる
document.getElementById('last-output').textContent = names[names.length - 1].textContent;


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
