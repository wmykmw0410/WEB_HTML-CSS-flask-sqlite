// ============================================================
// フォームの送信を止める（submit + preventDefault）
// ============================================================
// ブラウザには、イベントごとに決まった「既定の動作」がある
//   - フォームの submit → 入力内容をサーバーに送信して、ページを移動（再読み込み）する
//   - リンクの click   → href のページに移動する
// event.preventDefault() を呼ぶと、その既定の動作を止められる
const stopForm = document.getElementById('stop-form');
const stopTitle = document.getElementById('stop-title');
const stopOutput = document.getElementById('stop-output');

// ボタンの click ではなく、フォームの submit を監視する（Enterキーでの送信も拾える）
stopForm.addEventListener('submit', (event) => {
    event.preventDefault();   // ページの再読み込みを止める

    // 止めたあとは、JavaScript で好きな処理ができる
    stopOutput.textContent = `「${stopTitle.value}」を受け取りました（送信はしていません）`;
});

// 試してみよう：event.preventDefault(); の行をコメントアウトして、もう一度送信してみる
//   → ページが再読み込みされ、結果の表示がすぐに消える
