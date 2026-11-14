const memos = [
    { title: '買い物リスト', category: '家事' },
    { title: '企画会議メモ', category: '仕事' },
    { title: '読書メモ：銀河鉄道の夜', category: '趣味' },
];


// TODO 1：memos を、#memo-list の中に li として追加する
//         各 li は <span class="tag">カテゴリ</span> のあとにタイトルが続く形にする


// ============================================================
// テスト（ここから下は書き換えない）
// ============================================================
// ページの下の「テストを実行」ボタンを押すと、イベントが自動で起こされ、結果がConsoleに表示される
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

// イベントを自動で起こす（click・keydown・submit など）
const fire = (target, type, init = {}) => {
    const noBubble = ['mouseenter', 'mouseleave', 'focus', 'blur'].includes(type);
    const options = { bubbles: !noBubble, cancelable: true, ...init };
    let event;
    if (type === 'keydown') {
        event = new KeyboardEvent(type, options);
    } else if (type === 'click' || type.startsWith('mouse')) {
        event = new MouseEvent(type, options);
    } else {
        event = new Event(type, options);
    }
    target.dispatchEvent(event);
    return event;
};

const runTests = () => {
    const items = document.querySelectorAll('#memo-list li');
    check('TODO 1：li が3つ', items.length, 3);
    const tags = Array.from(items).map((li) => (li.querySelector('span.tag') ? li.querySelector('span.tag').textContent : '（span.tag なし）'));
    check('TODO 1：カテゴリのバッジ（span.tag）', tags, ['家事', '仕事', '趣味']);
    check('TODO 1：li の文字（バッジ＋タイトル）', Array.from(items).map((li) => li.textContent), ['家事買い物リスト', '仕事企画会議メモ', '趣味読書メモ：銀河鉄道の夜']);
};

const testButton = document.createElement('button');
testButton.type = 'button';
testButton.textContent = 'テストを実行（結果はConsoleに表示）';
document.body.append(testButton);
testButton.addEventListener('click', runTests);
if (location.search.includes('autorun')) {
    runTests();
}
