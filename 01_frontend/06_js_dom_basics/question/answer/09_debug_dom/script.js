// 解答9：書き換わらないページを直す

// バグ2：id の綴りが違っていた（mesage → message）。
//        取得できないと null になり、次の行で「Cannot set properties of null」になる
const message = document.getElementById('message');
message.textContent = 'JavaScriptで書き換えました';

const price = 300;
const quantity = 4;
const total = document.getElementById('total');

// バグ3：プロパティ名の大文字小文字が違っていた（textcontent → textContent）。
//        エラーは出ないが、存在しないプロパティに代入しただけなので、画面は変わらない
total.textContent = `合計：${price * quantity}円`;
