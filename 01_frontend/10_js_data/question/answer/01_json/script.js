/*
解答1：JSONの読み書き
*/

const user = { name: '山田', age: 20, hobbies: ['読書', '散歩'] };

// TODO 1
console.log(JSON.stringify(user));


const text = '[{"title": "買い物リスト", "pinned": true}, {"title": "企画会議メモ", "pinned": false}]';

// TODO 2
const memos = JSON.parse(text);
console.log(memos[1].title);

// TODO 3
console.log(memos.filter((memo) => memo.pinned).length);

// TODO 4
// 間違いは3つ：
//   1. キーがシングルクォート 'city' → JSONではダブルクォート "city" が必須
//   2. 文字列の値もシングルクォート '東京' → "東京"
//   3. 最後の要素の後ろにカンマ ,} → JSONでは最後のカンマは書けない
const broken = "{'city': '東京', 'zip': '100-0001',}";
const fixed = '{"city": "東京", "zip": "100-0001"}';
console.log(JSON.parse(fixed).city);
