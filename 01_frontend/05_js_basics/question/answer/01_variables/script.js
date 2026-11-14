/*
解答：小問1 変数とデータ型
*/

// TODO 1：書き換えない値なので const
const userName = '山田';


// TODO 2：あとで値を変えるので let。let は再代入できる（const はできない）
let score = 50;
score = 80;


// TODO 3：オブジェクトの値の書き換えは、ドット（.）で書く
const memo = { title: '会議', pinned: false };
memo.pinned = true;                // const でも、中身の書き換えはできる（禁止されるのは再代入だけ）


// TODO 4：配列は [] の中に , で区切って並べる
const tags = ['仕事', '重要'];


// TODO 5：${ } の中には、変数だけでなく tags.length のような式も書ける
const message = `${userName}さんのタグは${tags.length}個です`;


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

check('TODO 1：userName', get(() => userName), '山田');
check('TODO 2：score', get(() => score), 80);
check('TODO 3：memo.title', get(() => memo.title), '会議');
check('TODO 3：memo.pinned', get(() => memo.pinned), true);
check('TODO 4：tags', get(() => tags), ['仕事', '重要']);
check('TODO 5：message', get(() => message), '山田さんのタグは2個です');
