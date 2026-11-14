// 解答7：追記する・消す・置き換える

// TODO 1：+= で、今の文字の後ろに追加する（2回書く）
const log = document.getElementById('log-output');
log.textContent += ' → 次';
log.textContent += ' → 終了';


// TODO 2：空文字を代入すると、中身が消える
document.getElementById('temp-output').textContent = '';


// TODO 3：textContent を書き換えると、子要素もすべて消えて、文字だけになる
document.getElementById('box').textContent = '置き換えました';


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

check('TODO 1：#log-output', text('log-output'), '開始 → 次 → 終了');
check('TODO 2：#temp-output', text('temp-output'), '');
check('TODO 3：#box の文字', text('box'), '置き換えました');
check('TODO 3：#box の中の span', document.querySelectorAll('#box span').length, 0);
