// TODO 1：function 宣言で double(n) を書く。n を2倍にして返す
function double(n) {
}


// TODO 2：アロー関数（{ } と return を使う書き方）で add(a, b) を書く。a と b の合計を返す
const add = (a, b) => {
};


// TODO 3：アロー関数（{ } と return を省略した、1行の書き方）で square(n) を書く。n の2乗を返す
const square = (n) => {
};


// TODO 4：アロー関数で greet(name) を書く。「こんにちは、山田さん」のような文字を返す（テンプレートリテラル）
const greet = (name) => {
};


// TODO 5：アロー関数で average(a, b) を書く。a と b の平均を返す
const average = (a, b) => {
};


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
