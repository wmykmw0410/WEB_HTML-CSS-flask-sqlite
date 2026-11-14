// ============================================================
// DOM の最小限：「取得」と「書き換え」
// ============================================================
// ブラウザは、読み込んだHTMLを、JavaScriptから操作できる形（DOM）で持っている。
// DOM を使った操作は、次の2ステップだけでできる
//   ① 取得    ：document.getElementById('id') で、HTML の id が一致する要素を1つ手に入れる
//   ② 書き換え：要素.textContent に文字を入れると、画面の文字がすぐ変わる


// ============================================================
// 1. 取得して、書き換える
// ============================================================
const message = document.getElementById('message');   // ① 取得
message.textContent = 'JavaScriptで書き換えました';       // ② 書き換え

// 書き換えるだけでなく、読み取ることもできる
console.log(message.textContent);   // JavaScriptで書き換えました

// 見出しも、同じ書き方で書き換えられる（どの要素でも同じ）
const pageTitle = document.getElementById('page-title');
pageTitle.textContent = 'ページの文字を書き換えた（見出し）';


// ============================================================
// 2. 変数の値を表示する
// ============================================================
// テンプレートリテラルを使えば、計算結果も表示できる
const price = 300;
const count = 4;
const totalOutput = document.getElementById('total-output');
totalOutput.textContent = `${price}円 × ${count}個 = ${price * count}円`;


// ============================================================
// 3. Consoleから書き換えてみる
// ============================================================
// Console に直接
//   document.getElementById('console-target').textContent = 'Consoleから書き換えました'
// と打ち込んでも、同じように画面が書き換わる。
// 「書き換え」が、いつ実行されるか（ページを開いたとき・Consoleに打ち込んだとき）だけが違う。
// 次の07_js_eventsでは、これを「ボタンを押したとき」に実行する（イベント）。
