// ============================================================
// 1. trim()：文字列の前後の空白を取り除く
// ============================================================
console.log('  メモ '.trim());          // 'メモ'（前後の空白が消える）
console.log('   '.trim() === '');      // true（空白だけの入力は、空文字になる）


// ============================================================
// 2. 送信前に入力をチェックする
// ============================================================
const form = document.getElementById('name-form');
const nameInput = document.getElementById('name');
const nameError = document.getElementById('name-error');
const result = document.getElementById('result');

form.addEventListener('submit', (event) => {
    // このページには送信先が無いので、チェック結果にかかわらず送信は止める
    event.preventDefault();

    // 入力欄の値の前後の空白を取り除いてから調べる
    const name = nameInput.value.trim();

    if (name === '') {
        nameError.textContent = 'ニックネームを入力してください';
        result.textContent = '';
        return;   // ここで関数を終わる。これより下の「成功の処理」は実行されない
    }

    if (name.length > 10) {
        nameError.textContent = 'ニックネームは10文字以内で入力してください';
        result.textContent = '';
        return;
    }

    // ここまで来たら、問題なし
    nameError.textContent = '';
    result.textContent = `登録しました：${name}`;
});

// 補足：HTML の required 属性でも空欄は防げるが、空白だけの入力（'   '）は通ってしまう。
// JavaScript なら trim() を使った細かいチェックができる。
// ただし JavaScript のチェックもブラウザ側だけのもので、無効にできてしまうため、
// 02_backend/09_forms でサーバー（Python）側でも必ずチェックする
