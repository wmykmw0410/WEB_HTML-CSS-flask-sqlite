// ============================================================
// 1. 1つの要素を取得する
// ============================================================
// getElementById('id')      ：id が一致する要素を1つ取得する（# は付けない）
// querySelector('セレクタ')  ：CSS のセレクタに一致する「最初の」要素を1つ取得する
//                             03_css_basics で学んだセレクタが、そのまま使える
const byId = document.getElementById('heading');             // <h2 id="heading">
const byIdSelector = document.querySelector('#heading');     // id は # で指定する（同じ要素が取れる）
const byClass = document.querySelector('.note');             // クラスは . で指定する
const byTag = document.querySelector('h1');                  // タグ名はそのまま書く

console.log(byId === byIdSelector);   // true（どちらも同じ要素）

byClass.textContent = 'querySelector で取得して、書き換えました';

const singleOutput = document.getElementById('single-output');
singleOutput.textContent = `見出しの文字：${byId.textContent} / h1の文字：${byTag.textContent}`;


// ============================================================
// 2. 複数の要素を取得する
// ============================================================
// getElementsByClassName('クラス名') ：クラスが一致する要素「すべて」（HTMLCollection）
// getElementsByTagName('タグ名')     ：タグ名が一致する要素「すべて」（HTMLCollection）
// querySelectorAll('セレクタ')       ：セレクタに一致する要素「すべて」（NodeList）
//
// どれも「配列に似たもの」が返る。次のように使える
//   .length   … 要素の数
//   [0]       … 最初の要素（番号は 0 から。Python のリストと同じ）
//   [i]       … i 番目の要素

const names = document.getElementsByClassName('name');
console.log(names.length);                // 3
console.log(names[0].textContent);        // りんご（最初の要素）

// for 文で、1つずつ書き換える（HTMLCollection には forEach が無いので、for 文を使う）
for (let i = 0; i < names.length; i++) {
    names[i].textContent = `${i + 1}. ${names[i].textContent}`;
}

// querySelectorAll の結果（NodeList）は forEach が使える
const prices = document.querySelectorAll('.price');
prices.forEach((price) => {
    price.textContent += '円';           // += で、今の文字の後ろに追加する
});

const items = document.getElementsByTagName('li');
const multiOutput = document.getElementById('multi-output');
multiOutput.textContent = `商品は${items.length}個です`;


// ============================================================
// 3. 見つからないとき
// ============================================================
// 1つを取得する方法は null、すべてを取得する方法は「空」になる
console.log(document.getElementById('nothing'));              // null
console.log(document.querySelector('.nothing'));              // null
console.log(document.querySelectorAll('.nothing').length);    // 0
console.log(document.getElementsByClassName('nothing').length);  // 0

// null の textContent は読めないので、見つからない要素を書き換えようとするとエラーになる
// document.querySelector('.nothing').textContent = 'x';   // TypeError: Cannot set properties of null
