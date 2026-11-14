// 解答8：要素を取得して書き換える（まとめ）

// TODO 1：クラスは . を付ける
document.querySelector('.page-title').textContent = '商品一覧';


// TODO 2：getElementsByClassName の結果は .length で数を調べられる
const items = document.getElementsByClassName('item');
document.getElementById('count-output').textContent = `${items.length}個`;


// TODO 3：[0] で最初の要素を取り出す
const names = document.getElementsByClassName('name');
document.getElementById('first-output').textContent = names[0].textContent;


// TODO 4：textContent で読んだ価格は文字列なので、Number() で数値にしてから足す
const prices = document.querySelectorAll('.price');
let sum = 0;
prices.forEach((price) => {
    sum += Number(price.textContent);
});
document.getElementById('sum-output').textContent = `${sum}円`;


// TODO 5：合計の計算が終わってから「円」を付ける（先に付けると、Number('120円') が計算できなくなる）
prices.forEach((price) => {
    price.textContent += '円';
});


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
