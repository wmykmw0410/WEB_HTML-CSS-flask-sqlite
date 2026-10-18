// ============================================================
// 1. 配列のよく使うメソッド
// ============================================================
const memos = [
    { id: 1, title: '買い物リスト', category: '家事', pinned: true },
    { id: 2, title: '企画会議メモ', category: '仕事', pinned: false },
    { id: 3, title: '読書メモ：銀河鉄道の夜', category: '趣味', pinned: false },
    { id: 4, title: '資料作成', category: '仕事', pinned: true },
];

// map()：各要素を変換した「新しい配列」を作る
const titles = memos.map((memo) => memo.title);
console.log(titles);   // ['買い物リスト', '企画会議メモ', '読書メモ：銀河鉄道の夜', '資料作成']

// filter()：条件に合う要素だけの「新しい配列」を作る
const pinned = memos.filter((memo) => memo.pinned);
console.log(pinned.length);   // 2

// find()：条件に合う「最初の1件」を返す（見つからなければ undefined）
const memo3 = memos.find((memo) => memo.id === 3);
console.log(memo3.title);     // 読書メモ：銀河鉄道の夜
console.log(memos.find((memo) => memo.id === 99));   // undefined

// includes()：その値が含まれているか（true / false）
const categories = memos.map((memo) => memo.category);
console.log(categories.includes('仕事'));   // true
console.log(categories.includes('旅行'));   // false

// 組み合わせる：「仕事」カテゴリのメモのタイトルだけを取り出す
const workTitles = memos
    .filter((memo) => memo.category === '仕事')
    .map((memo) => memo.title);
console.log(workTitles);      // ['企画会議メモ', '資料作成']

// 文字列の includes() もある（部分一致の検索に使える）
console.log('企画会議メモ'.includes('会議'));   // true


// ============================================================
// 2. forEach / map / filter の使い分け
// ============================================================
// forEach：1件ずつ「何かをする」（画面を書き換える・ログを出す）。戻り値は無い
// map    ：1件ずつ「変換して」新しい配列を作る
// filter ：1件ずつ「残すかどうか判定して」新しい配列を作る
// find   ：条件に合う1件を探す
