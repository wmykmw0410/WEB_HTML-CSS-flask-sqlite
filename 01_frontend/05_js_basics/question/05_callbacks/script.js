const items = [
    { name: '買い物リスト', pinned: true },
    { name: '企画会議メモ', pinned: false },
    { name: '読書メモ', pinned: true },
];


// TODO 1
const countIf = (list, test) => {
};


// TODO 2
// どちらも「関数そのもの」か「呼び出した結果」かを間違えている。() を足すか消すかして直す
const getToday = () => '2026-10-03';
const todayText = getToday;

let hiCount = 0;
const sayHi = () => {
    hiCount++;
};
const runTwice = (callback) => {
    callback();
    callback();
};
const runSayHi = () => {
    runTwice(sayHi());
};


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

check('TODO 1：countIf(数値)', () => countIf([3, 8, 1, 6], (n) => n > 4), 2);
check('TODO 1：countIf(ピン留め)', () => countIf(items, (item) => item.pinned), 2);
check('TODO 1：countIf(0件)', () => countIf(items, (item) => item.name === '存在しない'), 0);
check('TODO 2：todayText', () => todayText, '2026-10-03');
check('TODO 2：runSayHi', () => {
    hiCount = 0;
    runSayHi();
    return hiCount;
}, 2);
