// TODO 1：trimText(text)：text の前後の空白を取り除いた文字を返す
const trimText = (text) => {
};


// TODO 2：isBlank(text)：text が、空、または空白だけなら true、そうでなければ false を返す
const isBlank = (text) => {
};


// TODO 3：hasEnough(text, min)：前後の空白を取り除いたあとの文字数が、min 以上なら true、そうでなければ false を返す
const hasEnough = (text, min) => {
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

// id から、要素の文字を取り出す（要素が無いときは目印の文字を返す）
const text = (id) => {
    const el = document.getElementById(id);
    return el ? el.textContent : '（その id の要素が無い）';
};

const get = (fn) => {
    try {
        return fn();
    } catch (error) {
        return '（未定義・エラー）';
    }
};

check('TODO 1：trimText(\'  メモ \')', get(() => trimText('  メモ ')), 'メモ');
check('TODO 1：trimText(\'abc\')', get(() => trimText('abc')), 'abc');
check('TODO 2：isBlank(\'\')', get(() => isBlank('')), true);
check('TODO 2：isBlank(\'   \')', get(() => isBlank('   ')), true);
check('TODO 2：isBlank(\' メモ \')', get(() => isBlank(' メモ ')), false);
check('TODO 3：hasEnough(\'あいうえお\', 5)', get(() => hasEnough('あいうえお', 5)), true);
check('TODO 3：hasEnough(\'  あい  \', 5)', get(() => hasEnough('  あい  ', 5)), false);
check('TODO 3：hasEnough(\'あいうえ\', 5)', get(() => hasEnough('あいうえ', 5)), false);