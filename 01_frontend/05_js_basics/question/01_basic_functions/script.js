// TODO 1
const getGrade = (score) => {
};


// TODO 2
const formatMemo = (memo) => {
};


// TODO 3
const sumTo = (n) => {
};


// TODO 4
const isFilled = (text) => {
};


// TODO 5
const countByCategory = (memos, category) => {
};


// TODO 6
const describeList = (list) => {
};


// ============================================================
// テスト（ここから下は書き換えない）
// ============================================================
const check = (label, actual, expected) => {
    const ok = JSON.stringify(actual) === JSON.stringify(expected);
    if (ok) {
        console.log(`✅ ${label}`);
    } else {
        console.log(`❌ ${label}　結果：${JSON.stringify(actual)}　期待：${JSON.stringify(expected)}`);
    }
};

const memos = [
    { id: 1, title: '買い物リスト', category: '家事' },
    { id: 2, title: '企画会議メモ', category: '仕事' },
    { id: 3, title: '資料作成', category: '仕事' },
];

check('TODO 1：getGrade(95)', getGrade(95), '合格');
check('TODO 1：getGrade(80)', getGrade(80), '合格');
check('TODO 1：getGrade(50)', getGrade(50), 'もう少し');
check('TODO 1：getGrade(10)', getGrade(10), '不合格');
check('TODO 2：formatMemo', formatMemo(memos[1]), '[仕事] 企画会議メモ');
check('TODO 3：sumTo(3)', sumTo(3), 6);
check('TODO 3：sumTo(10)', sumTo(10), 55);
check('TODO 4：isFilled(\'メモ\')', isFilled('メモ'), true);
check('TODO 4：isFilled(\'\')', isFilled(''), false);
check('TODO 5：countByCategory(仕事)', countByCategory(memos, '仕事'), 2);
check('TODO 5：countByCategory(趣味)', countByCategory(memos, '趣味'), 0);
check('TODO 6：describeList(memos)', describeList(memos), '3件のメモがあります');
check('TODO 6：describeList([])', describeList([]), 'メモはありません');
