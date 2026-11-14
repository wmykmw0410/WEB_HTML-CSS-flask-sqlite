// 解答5：複数の要素をまとめて書き換える

// TODO 1：querySelectorAll の結果（NodeList）は forEach が使える。文字は += ではなく、前に付けたいので作り直す
const fruits = document.querySelectorAll('.fruit');
fruits.forEach((fruit) => {
    fruit.textContent = `・${fruit.textContent}`;
});


// TODO 2：getElementsByClassName の結果（HTMLCollection）は forEach が無いので、for 文を使う
//         要素は [i]、番号は 0 から始まるので、表示は i + 1
const vegs = document.getElementsByClassName('veg');
for (let i = 0; i < vegs.length; i++) {
    vegs[i].textContent = `${i + 1}. ${vegs[i].textContent}`;
}


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
check('TODO 1：.fruit', texts('.fruit'), ['・りんご', '・バナナ', '・みかん']);
check('TODO 2：.veg', texts('.veg'), ['1. にんじん', '2. だいこん', '3. ねぎ']);
