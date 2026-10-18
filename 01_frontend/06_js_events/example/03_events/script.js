// ============================================================
// 1. イベントオブジェクト
// ============================================================
// addEventListener のコールバック関数は、引数で「イベントオブジェクト」を受け取れる。
// 何が起きたか（どの要素で・どのキーが押されたか など）の情報が入っている
const clickOutput = document.getElementById('click-output');

// ボタン1つずつではなく、親の #buttons に1回だけ登録する（イベントは親要素にも伝わる）
document.getElementById('buttons').addEventListener('click', (event) => {
    // event.target：実際にクリックされた要素
    const button = event.target.closest('button');   // closest()：自分または祖先から、セレクタに合う最も近い要素を探す
    if (!button) {
        return;   // ボタンとボタンの間の余白がクリックされた場合は何もしない
    }
    clickOutput.textContent = `${button.dataset.color}のボタンが押されました（event.type = ${event.type}）`;
});

// キーボードのイベント
const keyOutput = document.getElementById('key-output');
document.getElementById('key-input').addEventListener('keydown', (event) => {
    keyOutput.textContent = `押されたキー：${event.key}`;
});


// ============================================================
// 2. フォームの送信を止める（submit + preventDefault）
// ============================================================
// ブラウザには、イベントごとに決まった「既定の動作」がある
//   - フォームの submit → 入力内容をサーバーに送信してページを移動する
//   - リンクの click   → href のページに移動する
// event.preventDefault() を呼ぶと、その既定の動作を止められる
const form = document.getElementById('memo-form');
const titleInput = document.getElementById('title');
const titleError = document.getElementById('title-error');
const formOutput = document.getElementById('form-output');

// ボタンの click ではなく、フォームの submit を監視する（Enterキーでの送信も拾える）
form.addEventListener('submit', (event) => {
    if (!titleInput.value.trim()) {
        event.preventDefault();   // 送信を止める
        titleError.textContent = 'タイトルを入力してください（空白だけは不可）';
        return;
    }
    // 本来はここで送信される。このサンプルでは送信先が無いので、送信も止めて結果だけ表示する
    event.preventDefault();
    titleError.textContent = '';
    formOutput.textContent = `「${titleInput.value}」を送信します（このサンプルでは実際には送信しません）`;
});

// 補足：required 属性でも空欄は防げるが、空白だけの入力（'   '）は通ってしまう。
// JavaScript なら trim() を使った細かいチェックができる。
// ただし JavaScript のチェックもブラウザ側だけのもので、無効にできてしまうため、
// 02_backend/09_forms でサーバー（Python）側でも必ずチェックする


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
// 4. ホバー（マウスを乗せる）とフォーカス
// ============================================================
// 見た目を変えるだけなら CSS の :hover で十分。
// 「中身を書き換える」「別の要素を表示する」など、CSS だけではできないことを JavaScript で行う
document.querySelectorAll('[data-tip]').forEach((button) => {
    // ツールチップの要素を作って、ボタンの中に入れておく（最初は hidden で隠す）
    const tip = document.createElement('span');
    tip.className = 'tooltip';
    tip.textContent = button.dataset.tip;
    tip.hidden = true;
    button.append(tip);

    const show = () => { tip.hidden = false; };
    const hide = () => { tip.hidden = true; };

    // mouseenter：マウスが要素に入ったとき ／ mouseleave：出たとき
    button.addEventListener('mouseenter', show);
    button.addEventListener('mouseleave', hide);

    // focus：Tab キーなどで要素が選ばれたとき ／ blur：選択が外れたとき
    // マウスを使わない人にも同じ情報を届けるため、ホバーとセットで書く
    button.addEventListener('focus', show);
    button.addEventListener('blur', hide);
});

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
