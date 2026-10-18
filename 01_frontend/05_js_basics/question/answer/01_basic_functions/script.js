/*
解答1：基本文法で関数を書く
*/


// TODO 1：上の条件から順に判定される。80点以上は最初の if で決まるので、
//         else if では「50点以上」だけを書けばよい（80未満であることは確定している）
const getGrade = (score) => {
    if (score >= 80) {
        return '合格';
    } else if (score >= 50) {
        return 'もう少し';
    } else {
        return '不合格';
    }
};


// TODO 2：テンプレートリテラルの ${} の中には、変数だけでなく memo.title のような式も書ける
const formatMemo = (memo) => {
    return `[${memo.category}] ${memo.title}`;
};
// 1行で書くなら：const formatMemo = (memo) => `[${memo.category}] ${memo.title}`;


// TODO 3：total は値が変わるので let。i <= n にしないと n が足されない
const sumTo = (n) => {
    let total = 0;
    for (let i = 1; i <= n; i++) {
        total += i;              // total = total + i; と同じ
    }
    return total;
};


// TODO 4：空文字でないかを比べ、その結果（true / false）をそのまま返す
const isFilled = (text) => {
    return text !== '';
};
// 別解：if (text) { return true; } return false;
//       （空文字は falsy なので、if の条件にそのまま書ける）


// TODO 5：数える変数は let、比べるときは ===
const countByCategory = (memos, category) => {
    let count = 0;
    memos.forEach((memo) => {
        if (memo.category === category) {
            count++;
        }
    });
    return count;
};
// 2節の filter を使うと：return memos.filter((memo) => memo.category === category).length;


// TODO 6：空かどうかは length で判定する（[] は truthy なので if (list) だと常に真になる）
const describeList = (list) => {
    if (list.length === 0) {
        return 'メモはありません';
    }
    return `${list.length}件のメモがあります`;
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
