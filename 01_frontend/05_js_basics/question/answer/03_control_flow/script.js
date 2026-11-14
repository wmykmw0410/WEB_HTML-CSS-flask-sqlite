/*
解答：小問3 条件分岐・繰り返し・配列
*/

// TODO 1：上の条件から順に判定される。else if では「0」だけ書けばよい
const signOf = (n) => {
    if (n > 0) {
        return '正';
    } else if (n === 0) {
        return 'ゼロ';
    } else {
        return '負';
    }
};


// TODO 2：比較は === 。結果（true / false）をそのまま返せる
const isSame = (a, b) => {
    return a === b;
};


// TODO 3：文字を入れる変数は、あとで足していくので let。+= で後ろにつなげる
const repeatText = (text, times) => {
    let result = '';
    for (let i = 0; i < times; i++) {
        result += text;
    }
    return result;
};


// TODO 4：合計を入れる変数は let。forEach のコールバックの中で足す
const sum = (list) => {
    let total = 0;
    list.forEach((n) => {
        total += n;
    });
    return total;
};


// TODO 5：push で追加した後の件数は、list.length で分かる
const addItem = (list, item) => {
    list.push(item);
    return list.length;
};


// TODO 6：新しい配列は const で空の配列を用意し、forEach の中で push する（const でも push はできる）
const getTitles = (memos) => {
    const titles = [];
    memos.forEach((memo) => {
        titles.push(memo.title);
    });
    return titles;
};


// ============================================================
// テスト（ここから下は書き換えない）
// ============================================================
// まだ書いていない（宣言されていない）変数や関数があっても、他のテストは続けて実行する
const get = (fn) => {
    try {
        return fn();
    } catch (error) {
        return '（未定義・エラー）';
    }
};

const check = (label, actual, expected) => {
    const ok = JSON.stringify(actual) === JSON.stringify(expected);
    if (ok) {
        console.log(`✅ ${label}`);
    } else {
        console.log(`❌ ${label}　結果：${JSON.stringify(actual)}　期待：${JSON.stringify(expected)}`);
    }
};

check('TODO 1：signOf(5)', get(() => signOf(5)), '正');
check('TODO 1：signOf(0)', get(() => signOf(0)), 'ゼロ');
check('TODO 1：signOf(-2)', get(() => signOf(-2)), '負');
check('TODO 2：isSame(2, 2)', get(() => isSame(2, 2)), true);
check('TODO 2：isSame(1, \'1\')', get(() => isSame(1, '1')), false);
check('TODO 3：repeatText(\'ab\', 3)', get(() => repeatText('ab', 3)), 'ababab');
check('TODO 3：repeatText(\'x\', 0)', get(() => repeatText('x', 0)), '');
check('TODO 4：sum([1, 2, 3])', get(() => sum([1, 2, 3])), 6);
check('TODO 4：sum([])', get(() => sum([])), 0);
check('TODO 5：addItem([\'a\'], \'b\')', get(() => addItem(['a'], 'b')), 2);
check('TODO 6：getTitles', get(() => getTitles([{ title: '会議' }, { title: '買い物' }])), ['会議', '買い物']);
check('TODO 6：getTitles([])', get(() => getTitles([])), []);
