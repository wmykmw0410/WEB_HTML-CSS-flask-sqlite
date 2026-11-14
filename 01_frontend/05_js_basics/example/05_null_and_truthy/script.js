// ============================================================
// 1. 「値が無い」ことを表す null と undefined
// ============================================================
let notAssigned;                                   // 宣言だけして値を入れていない変数
console.log(notAssigned);                          // undefined（まだ値が入っていない）

// null は「無い」ことを意図的に表す値（例：まだ何も選ばれていない）
const selected = null;
console.log(selected);                             // null
// （06章で学ぶ document.getElementById() も、要素が見つからないと null を返す）

// null のプロパティを読もうとするとエラーになる（コメントを外すと Console に赤字のエラーが出る）
// console.log(selected.title);   // TypeError: Cannot read properties of null (reading 'title')


// ============================================================
// 2. 真偽の判定：truthy と falsy
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

// この性質を使うと「値があるときだけ処理する」が短く書ける
// （10章のHPで使う if (要素) { ... } はこの書き方）
if (selected) {
    console.log('値がある');
} else {
    console.log('値が無い（null）ので何もしない');
}

// 入力欄が空かどうかの判定にも使える（空文字は falsy）
const input = '';
if (input) {
    console.log('入力あり');
} else {
    console.log('空欄');   // 空欄
}


// ============================================================
// 3. == は使わない
// ============================================================
// == は型を自動で変換してから比べるので、思わぬ結果になる
console.log(1 == '1');            // true（文字列 '1' を数値に変換してから比べている）
console.log(0 == '');             // true
console.log(null == undefined);   // true

// === は型も含めて比べる。基本的には常にこちらを使う
console.log(1 === '1');           // false
console.log(0 === '');            // false

// 補足：古いコードでは変数の宣言に var が使われていることがあるが、
// 予期しない動きをしやすいため、今は let / const だけを使う
