// TODO 1：signOf(n)：n が 0 より大きければ '正'、0 ならば 'ゼロ'、それ以外は '負' を返す
const signOf = (n) => {
};


// TODO 2：isSame(a, b)：a と b が等しい（型も含めて）かを true / false で返す
const isSame = (a, b) => {
};


// TODO 3：repeatText(text, times)：text を times 回つなげた文字を返す（for 文を使う）
const repeatText = (text, times) => {
};


// TODO 4：sum(list)：配列の数値をすべて足した合計を返す（forEach を使う）
const sum = (list) => {
};


// TODO 5：addItem(list, item)：配列 list の最後に item を追加して、追加後の件数を返す
const addItem = (list, item) => {
};


// TODO 6：getTitles(memos)：メモの配列から、title だけを取り出した新しい配列を返す（forEach と push を使う）
const getTitles = (memos) => {
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
