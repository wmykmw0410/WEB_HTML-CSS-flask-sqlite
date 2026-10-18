// 解答3：フォームの送信前に入力をチェックする

const form = document.getElementById('memo-form');
const titleInput = document.getElementById('title');
const bodyInput = document.getElementById('body');
const titleError = document.getElementById('title-error');
const bodyError = document.getElementById('body-error');
const result = document.getElementById('result');


// TODO 1：エラー表示を切り替える関数
const showError = (input, errorEl, message) => {
    errorEl.textContent = message;
    input.classList.toggle('invalid', message !== '');
};


// TODO 2：submit で入力をチェックする
form.addEventListener('submit', (event) => {
    // このページには送信先が無いので、チェック結果にかかわらず送信は止める
    // （実際のアプリでは、エラーがあるときだけ preventDefault() する）
    event.preventDefault();

    const title = titleInput.value.trim();
    const body = bodyInput.value.trim();

    const titleMessage = title ? '' : 'タイトルを入力してください';
    const bodyMessage = body.length >= 10 ? '' : '本文は10文字以上で入力してください';

    showError(titleInput, titleError, titleMessage);
    showError(bodyInput, bodyError, bodyMessage);

    if (titleMessage || bodyMessage) {
        result.textContent = '';
        return;
    }

    result.textContent = `保存しました：${title}`;
});


// TODO 3：reset で確認する
form.addEventListener('reset', (event) => {
    const hasInput = titleInput.value || bodyInput.value;

    if (hasInput && !confirm('入力内容を消しますか？')) {
        event.preventDefault();   // キャンセル → 入力を消さない
        return;
    }

    showError(titleInput, titleError, '');
    showError(bodyInput, bodyError, '');
    result.textContent = '';
});
