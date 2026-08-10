// ============================================================
// 1. 変数：let と const
// ============================================================
let count = 1;       // 再代入できる変数
count = 2;            // OK

const name = 'メモ帳'; // 再代入できない変数（定数）
// name = '別の名前';  // これはエラーになる

console.log(count, name);

// Pythonと違い、変数の宣言には let か const が必要
// 何が変わるか分からない場合はまず const を使い、再代入が必要になったら let に変える


// ============================================================
// 2. データ型
// ============================================================
const str = 'こんにちは';      // 文字列（文字列は '' でも "" でも書ける）
const num = 42;                // 数値（整数もfloatも区別しない）
const isDone = true;           // 真偽値（true / false。Pythonの True / False とは大文字小文字が違う）
const list = [1, 2, 3];        // 配列（Pythonのlistに相当）
const obj = { title: 'メモ', category: '仕事' };   // オブジェクト（Pythonのdictに相当）

console.log(str, num, isDone, list, obj);

// テンプレートリテラル：バッククォート(`)で囲むと ${式} で変数を埋め込める
const message = `${name}には${list.length}件のメモがあります`;
console.log(message);   // メモ帳には3件のメモがあります


// ============================================================
// 3. 関数
// ============================================================
// 3-1. function 宣言
function add(a, b) {
    return a + b;
}

// 3-2. アロー関数（本章のサンプルで多用する書き方）
const addArrow = (a, b) => {
    return a + b;
};

// 処理が1行だけなら {} と return を省略できる
const addShort = (a, b) => a + b;

console.log(add(1, 2), addArrow(1, 2), addShort(1, 2));   // 3 3 3


// ============================================================
// 4. 条件分岐と繰り返し
// ============================================================
const score = 80;

if (score >= 80) {
    console.log('合格');
} else if (score >= 50) {
    console.log('もう少し');
} else {
    console.log('不合格');
}

// for文（Pythonのrange()に近い書き方）
for (let i = 0; i < 3; i++) {
    console.log(`ループ ${i} 回目`);
}

// 配列を1件ずつ処理する（Pythonの for x in list: に相当）
const categories = ['家事', '仕事', '趣味'];
categories.forEach((category) => {
    console.log(category);
});


// ============================================================
// 5. オブジェクトと配列の操作
// ============================================================
const memo = { title: '買い物リスト', category: '家事', pinned: false };

console.log(memo.title);       // ドット記法でプロパティにアクセス（memo['title']でも同じ）
memo.pinned = true;             // プロパティの書き換え
console.log(memo);

// 配列からオブジェクトのリストを作る例（このあとメモ一覧を扱うときによく出てくる形）
const memos = [
    { id: 1, title: '買い物リスト', category: '家事' },
    { id: 2, title: '企画会議メモ', category: '仕事' },
];

// filter()：条件に一致する要素だけを集めた新しい配列を作る
const workMemos = memos.filter((m) => m.category === '仕事');
console.log(workMemos);   // [{ id: 2, title: '企画会議メモ', category: '仕事' }]
