const message = document.getElementById('mesage');
message.textContent = 'JavaScriptで書き換えました';

const price = 300;
const quantity = 4;
const total = document.getElementById('total');
total.textcontent = `合計：${price * quantity}円`;
