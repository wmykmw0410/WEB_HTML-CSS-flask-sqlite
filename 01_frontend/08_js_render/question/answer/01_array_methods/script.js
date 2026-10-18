/*
解答1：配列メソッド
*/

const memos = [
    { id: 1, title: '買い物リスト', category: '家事', pinned: true },
    { id: 2, title: '企画会議メモ', category: '仕事', pinned: false },
    { id: 3, title: '読書メモ：銀河鉄道の夜', category: '趣味', pinned: false },
    { id: 4, title: '会議の議事録', category: '仕事', pinned: true },
    { id: 5, title: '旅行の持ち物リスト', category: 'プライベート', pinned: false },
];


// TODO 1：map は1件ずつ「変換」した新しい配列を返す
const ids = memos.map((memo) => memo.id);


// TODO 2：filter で残した配列の length。pinned は true / false なので、=== true と書かなくてよい
const pinnedCount = memos.filter((memo) => memo.pinned).length;


// TODO 3：find は条件に合う「最初の1件」を返す（配列ではない）。見つからなければ undefined
const findMemo = (id) => {
    return memos.find((memo) => memo.id === id);
};


// TODO 4：filter で絞り込んでから、map でタイトルだけに変換する
const searchTitles = (keyword) => {
    return memos
        .filter((memo) => memo.title.includes(keyword))
        .map((memo) => memo.title);
};


// TODO 5：まだ入っていないものだけ push する
//         categories は const だが、中身を push で増やすのは「再代入」ではないのでエラーにならない
const categories = [];
memos.forEach((memo) => {
    if (!categories.includes(memo.category)) {
        categories.push(memo.category);
    }
});


// ============================================================
// テスト（ここから下は書き換えない）
// ============================================================
// check(説明, 結果を返す関数, 期待する値)：途中でエラーが起きても、残りのテストは続けて実行する
const check = (label, getActual, expected) => {
    try {
        const actual = getActual();
        const ok = JSON.stringify(actual) === JSON.stringify(expected);
        if (ok) {
            console.log(`✅ ${label}`);
        } else {
            console.log(`❌ ${label}　結果：${JSON.stringify(actual)}　期待：${JSON.stringify(expected)}`);
        }
    } catch (error) {
        console.log(`❌ ${label}　エラー：${error.message}`);
    }
};

check('TODO 1：ids', () => ids, [1, 2, 3, 4, 5]);
check('TODO 2：pinnedCount', () => pinnedCount, 2);
check('TODO 3：findMemo(3)', () => findMemo(3), memos[2]);
check('TODO 3：findMemo(99)', () => findMemo(99), undefined);
check('TODO 4：searchTitles(会議)', () => searchTitles('会議'), ['企画会議メモ', '会議の議事録']);
check('TODO 4：searchTitles(リスト)', () => searchTitles('リスト'), ['買い物リスト', '旅行の持ち物リスト']);
check('TODO 5：categories', () => categories, ['家事', '仕事', '趣味', 'プライベート']);
check('元の memos が変更されていない', () => memos.length, 5);
