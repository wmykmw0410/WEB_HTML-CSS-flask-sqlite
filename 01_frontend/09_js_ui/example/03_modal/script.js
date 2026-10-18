const dialog = document.getElementById('work-dialog');
const dialogTitle = document.getElementById('dialog-title');
const dialogDetail = document.getElementById('dialog-detail');

// ============================================================
// 開く：中身を書き換えてから showModal() を呼ぶ
// ============================================================
document.getElementById('works').addEventListener('click', (event) => {
    const button = event.target.closest('button');
    if (!button) {
        return;
    }
    dialogTitle.textContent = button.dataset.title;
    dialogDetail.textContent = button.dataset.detail;
    dialog.showModal();   // モーダルとして開く（Esc キーで閉じる動作は、ブラウザが自動で付けてくれる）
});

// ============================================================
// 閉じる：close() を呼ぶ
// ============================================================
document.getElementById('dialog-close').addEventListener('click', () => {
    dialog.close();
});

// 暗い背景（::backdrop）をクリックしたときも閉じる
// 背景をクリックすると、event.target は <dialog> 自身になる（中身をクリックしたときは中の要素になる）
// そのため <dialog> 自体には padding を付けず、中身を .dialog-body で包んでいる
// （<dialog> に padding があると、その余白をクリックしたときも <dialog> 自身が target になって閉じてしまう）
dialog.addEventListener('click', (event) => {
    if (event.target === dialog) {
        dialog.close();
    }
});

// 補足：
//   - dialog.open で、今開いているか（true / false）がわかる
//   - 閉じたときに何かしたい場合は、dialog.addEventListener('close', () => { ... }) を使う
//   - モーダルを開くとフォーカスは自動でダイアログの中に移り、閉じると開く前の要素に戻る
//   - 開いている間は後ろのページがスクロールしないように、CSS で body:has(dialog[open]) { overflow: hidden; } を指定している
//   - 後ろを操作したまま出す「ポップアップ」は、02_popup の popover 属性を使う
