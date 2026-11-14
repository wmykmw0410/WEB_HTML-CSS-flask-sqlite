/*
解答：小問2 関数
*/

// TODO 1：値を返すときは return を書く
function double(n) {
    return n * 2;
}


// TODO 2：{ } を使う書き方では、return が必要
const add = (a, b) => {
    return a + b;
};


// TODO 3：{ } と return を省略すると、=> のあとの式がそのまま戻り値になる
const square = (n) => n * n;


// TODO 4：テンプレートリテラルをそのまま返す
const greet = (name) => `こんにちは、${name}さん`;


// TODO 5：足し算を ( ) で囲んでから割る（( ) が無いと、b だけが 2 で割られてしまう）
const average = (a, b) => (a + b) / 2;


// ============================================================
// テスト（ここから下は書き換えない）
// ============================================================
// まだ書いていない（宣言されていない）変数や関数があっても、他のテストは続けて実行する
const get = (fn) => {
    try {
        return fn();
    } catch (error) {
        return '（未定義・エラー）';
    }
};

const check = (label, actual, expected) => {
    const ok = JSON.stringify(actual) === JSON.stringify(expected);
    if (ok) {
        console.log(`✅ ${label}`);
    } else {
        console.log(`❌ ${label}　結果：${JSON.stringify(actual)}　期待：${JSON.stringify(expected)}`);
    }
};

check('TODO 1：double(4)', get(() => double(4)), 8);
check('TODO 2：add(1, 2)', get(() => add(1, 2)), 3);
check('TODO 2：add(10, -3)', get(() => add(10, -3)), 7);
check('TODO 3：square(5)', get(() => square(5)), 25);
check('TODO 4：greet(\'山田\')', get(() => greet('山田')), 'こんにちは、山田さん');
check('TODO 5：average(2, 4)', get(() => average(2, 4)), 3);
check('TODO 5：average(1, 2)', get(() => average(1, 2)), 1.5);
