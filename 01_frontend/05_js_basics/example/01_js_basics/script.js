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
const num = 42;                // 数値（整数と小数を区別しない）
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
console.log(memos.length);   // 2（配列の要素数は length。() は付けない）

// push()：配列の最後に要素を追加する（Pythonの append）
memos.push({ id: 3, title: '読書メモ', category: '趣味' });
console.log(memos.length);   // 3


// ============================================================
// 6. 「値が無い」ことを表す null と undefined
// ============================================================
let notAssigned;                                   // 宣言だけして値を入れていない変数
console.log(notAssigned);                          // undefined（まだ値が入っていない）

// document.getElementById() は、該当する要素が無いと null を返す
// （このページには id="body" の要素が無い）
const missing = document.getElementById('body');
console.log(missing);                              // null（「無い」ことを意図的に表す値）

// null のプロパティを読もうとするとエラーになる（コメントを外すと Console に赤字のエラーが出る）
// console.log(missing.value);   // TypeError: Cannot read properties of null (reading 'value')


// ============================================================
// 7. 真偽の判定：truthy と falsy
// ============================================================
// if の条件には true / false 以外の値も書ける。
// 次の値は「偽（falsy）」として扱われ、それ以外はすべて「真（truthy）」になる
//   false, 0, ''（空文字）, null, undefined, NaN
const values = [false, 0, '', null, undefined, 'a', 1, [], {}];
values.forEach((value) => {
    if (value) {
        console.log(value, '→ truthy');
    } else {
        console.log(value, '→ falsy');
    }
});

// この性質を使うと「要素があるときだけ処理する」が短く書ける
// （このあとの script.js で使う if (bodyTextarea) { ... } はこの書き方）
if (missing) {
    console.log('要素がある');
} else {
    console.log('要素が無いので何もしない');
}

// 入力欄が空かどうかの判定にも使える（空文字は falsy）
const input = '';
if (input) {
    console.log('入力あり');
} else {
    console.log('空欄');   // 空欄
}


// ============================================================
// 8. 比較は === を使う
// ============================================================
// == は型を自動で変換してから比べるので、思わぬ結果になる
console.log(1 == '1');       // true（文字列 '1' を数値に変換してから比べている）
console.log(0 == '');        // true
console.log(null == undefined);   // true

// === は型も含めて比べる。基本的には常にこちらを使う
console.log(1 === '1');      // false
console.log(0 === '');       // false
console.log(1 !== '1');      // true（!== は「等しくない」）

// 補足：古いコードでは変数の宣言に var が使われていることがあるが、
// 予期しない動きをしやすいため、今は let / const だけを使う
