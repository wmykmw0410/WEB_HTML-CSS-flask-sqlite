// ============================================================
// 1. 条件分岐と比較
// ============================================================
const score = 80;

if (score >= 80) {
    console.log('合格');
} else if (score >= 50) {
    console.log('もう少し');
} else {
    console.log('不合格');
}

// 比較は === を使う（等しくない場合は !==）
console.log(score === 80);    // true
console.log(score !== 80);    // false
console.log(1 === '1');       // false（型が違うので等しくない）


// ============================================================
// 2. 繰り返し
// ============================================================
// for文（Pythonのrange()に近い書き方）
for (let i = 0; i < 3; i++) {
    console.log(`ループ ${i} 回目`);
}

// 合計を求める：+= は「足して代入」、++ は「1増やす」
let total = 0;
for (let i = 1; i <= 3; i++) {
    total += i;                // total = total + i; と同じ
}
console.log(total);            // 6


// ============================================================
// 3. 配列
// ============================================================
const categories = ['家事', '仕事', '趣味'];
console.log(categories.length);   // 3（配列の要素数は length。() は付けない）

// 配列を1件ずつ処理する（Pythonの for x in list: に相当）
categories.forEach((category) => {
    console.log(category);
});

// push()：配列の最後に要素を追加する（Pythonの append）
categories.push('勉強');
console.log(categories.length);   // 4


// ============================================================
// 4. オブジェクトの配列
// ============================================================
// このあとメモ一覧を扱うときによく出てくる形
const memos = [
    { id: 1, title: '買い物リスト', category: '家事' },
    { id: 2, title: '企画会議メモ', category: '仕事' },
];

memos.forEach((memo) => {
    console.log(`${memo.id}：${memo.title}`);
});
