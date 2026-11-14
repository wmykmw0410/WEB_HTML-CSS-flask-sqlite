// ============================================================
// 1. 読み取る
// ============================================================
const unitPrice = document.getElementById('unit-price');
const readOutput = document.getElementById('read-output');

// textContent で読み取った値は、数字に見えても「文字列」
console.log(unitPrice.textContent);                 // '1000'（文字列）
console.log(unitPrice.textContent + 500);           // '1000500'（文字列の連結になってしまう）

// 計算に使うときは、Number() で数値に変換する（Python の int() / float() に近い）
const price = Number(unitPrice.textContent);
console.log(price + 500);                           // 1500

readOutput.textContent = `3個買うと ${price * 3}円`;   // 数値を埋め込んで、文字として表示する


// ============================================================
// 2. 追記する・消す
// ============================================================
const logOutput = document.getElementById('log-output');

logOutput.textContent = '1行目';                    // 書き換える（今の文字は消える）
logOutput.textContent += ' / 2行目';                // += で、今の文字の後ろに追加する
logOutput.textContent += ' / 3行目';
// logOutput.textContent = '';                      // 空文字を代入すると、中身を消せる（コメントを外してみる）


// ============================================================
// 3. タグを入れても、文字として表示される
// ============================================================
// textContent は、入れた文字列を「ただの文字」として扱う。<b> もタグとしては働かない
const tagOutput = document.getElementById('tag-output');
tagOutput.textContent = '<b>太字</b> を入れても、そのまま文字で表示される';
// HTML として解釈して入れる innerHTML もあるが、ユーザーの入力を入れると危険（XSS）。09_js_dom で学ぶ


// ============================================================
// 4. 子要素ごと置き換わる
// ============================================================
// 要素の textContent を書き換えると、その中にあった子要素（<span> など）も全部消えて、文字だけになる
const box = document.getElementById('box');
console.log(box.textContent);                       // 子要素1 子要素2（子要素の文字もまとめて読める）
box.textContent = '中身がすべて、この1つの文字に置き換わりました';
