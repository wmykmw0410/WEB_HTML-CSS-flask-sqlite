// TODO 1：クラスが fruit の要素を querySelectorAll ですべて取得し、forEach で1つずつ、文字の前に「・」を付ける
//         （「りんご」→「・りんご」）


// TODO 2：クラスが veg の要素を getElementsByClassName ですべて取得し、for 文で1つずつ、文字の前に番号を付ける
//         （「にんじん」→「1. にんじん」。番号は 1 から）


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
