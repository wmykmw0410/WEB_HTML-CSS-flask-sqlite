// ============================================================
// 1. 条件を組み合わせる：&&（かつ）・||（または）・!（でない）
// ============================================================
const isLoggedIn = true;
const isAdmin = false;

console.log(isLoggedIn && isAdmin);    // false（両方が true のときだけ true）
console.log(isLoggedIn || isAdmin);    // true （どちらかが true なら true）
console.log(!isAdmin);                 // true （true と false を入れ替える）


// ============================================================
// 2. 値を条件で選ぶ：三項演算子  条件 ? A : B
// ============================================================
// 条件が真なら A、偽なら B になる式。if / else で値を選ぶ処理を1行で書ける
const isDone = true;
const label = isDone ? '完了' : '未完了';
console.log(label);   // 完了

// 上は次の if / else と同じ
let label2;
if (isDone) {
    label2 = '完了';
} else {
    label2 = '未完了';
}
console.log(label2);  // 完了

// 入力チェックでは「エラーが無ければ空文字、あればエラー文」という形でよく使う
const title = '';
const titleMessage = title === '' ? 'タイトルを入力してください' : '';
console.log(titleMessage);   // タイトルを入力してください


// ============================================================
// 3. confirm() で確認する
// ============================================================
// confirm('メッセージ') は確認ダイアログを出し、OK なら true、キャンセルなら false を返す
document.getElementById('leave-link').addEventListener('click', (event) => {
    const ok = confirm('外部サイトに移動します。よろしいですか？');
    if (!ok) {
        event.preventDefault();   // キャンセルされたらリンクの移動を止める
    }
});

// HTML 側の onclick="return confirm('削除しますか？')" も同じ仕組み。
// onclick 属性の中で false を return すると、preventDefault() と同じく既定の動作（送信）が止まる。
// 削除ボタンでは、この短い書き方もよく使われる


// ============================================================
// 4. reset の前に確認する
// ============================================================
// reset は「入力を消す」という既定の動作を持つイベント。preventDefault() で止められる
const resetForm = document.getElementById('reset-form');
const resetInput = document.getElementById('reset-input');

resetForm.addEventListener('reset', (event) => {
    // 何か入力されている && 確認でキャンセルされた、ときだけ止める
    if (resetInput.value !== '' && !confirm('入力内容を消しますか？')) {
        event.preventDefault();
    }
});


// ============================================================
// 5. mouseover と mouseenter の違い
// ============================================================
// mouseover は「子要素に移るたび」にも発生する。mouseenter は「その要素に入ったとき」1回だけ
const hoverBox = document.getElementById('hover-box');
const hoverCount = document.getElementById('hover-count');
let overCount = 0;
let enterCount = 0;
const showCount = () => {
    hoverCount.textContent = `mouseover：${overCount}回 ／ mouseenter：${enterCount}回`;
};
hoverBox.addEventListener('mouseover', () => { overCount++; showCount(); });
hoverBox.addEventListener('mouseenter', () => { enterCount++; showCount(); });
