// ============================================================
// 1. JavaScriptのオブジェクト → JSON文字列（JSON.stringify）
// ============================================================
const memo = { id: 1, title: '買い物リスト', tags: ['家事', '急ぎ'], pinned: true };

const json = JSON.stringify(memo);
console.log(json);            // {"id":1,"title":"買い物リスト","tags":["家事","急ぎ"],"pinned":true}
console.log(typeof json);     // string（ただの文字列になった）

// 第3引数にスペースの数を渡すと、人間が読みやすいように改行・インデントしてくれる
console.log(JSON.stringify(memo, null, 2));


// ============================================================
// 2. JSON文字列 → JavaScriptのオブジェクト（JSON.parse）
// ============================================================
const text = '{"id": 2, "title": "企画会議メモ", "pinned": false}';
const parsed = JSON.parse(text);
console.log(parsed.title);    // 企画会議メモ（オブジェクトとして使える）
console.log(typeof parsed);   // object


// ============================================================
// 3. JSONの書き方のルール（JavaScriptのオブジェクトより厳しい）
// ============================================================
// - キーは必ずダブルクォート " で囲む
// - 文字列もダブルクォート "（シングルクォート ' は使えない）
// - 最後の要素の後ろにカンマを付けない
// - 使える値：文字列・数値・true/false・null・配列・オブジェクト（関数や undefined は使えない）

// ルール違反のJSONを parse するとエラーになる。try / catch で受け止められる
const broken = "{'title': 'シングルクォートは使えない'}";
try {
    JSON.parse(broken);
} catch (error) {
    console.log('JSONとして読めない：', error.message);
}


// ============================================================
// 4. 配列もそのままJSONにできる
// ============================================================
const memos = [
    { id: 1, title: '買い物リスト' },
    { id: 2, title: '企画会議メモ' },
];
const memosJson = JSON.stringify(memos);
console.log(memosJson);                       // [{"id":1,"title":"買い物リスト"},{"id":2,"title":"企画会議メモ"}]
console.log(JSON.parse(memosJson).length);    // 2（文字列 → 配列に戻った）
