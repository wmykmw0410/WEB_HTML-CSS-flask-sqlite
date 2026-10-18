/*
contact.js：お問い合わせ（contact.html）の動き

    1. 文字数カウンター … 06_js_events 2節
    2. 入力チェック     … submit・preventDefault（06_js_events 3節）
    3. 送信後の通知     … ポップアップ（popover="manual"）と setTimeout（09_js_ui 2節）
*/

const contactForm = document.getElementById('contact-form');

if (contactForm) {
    const name = document.getElementById('name');
    const email = document.getElementById('email');
    const message = document.getElementById('message');
    const counter = document.getElementById('message-count');
    const toast = document.getElementById('toast');
    let toastTimer = null;

    // ============================================================
    // 1. 文字数カウンター
    // ============================================================
    const updateCount = () => {
        counter.textContent = message.value.length;
    };
    message.addEventListener('input', updateCount);


    // ============================================================
    // 2. 入力チェック
    // ============================================================
    const showError = (input, text) => {
        document.getElementById(`${input.id}-error`).textContent = text;
        input.classList.toggle('invalid', text !== '');
    };

    // ============================================================
    // 3. 送信後の通知（3秒で自動的に消える）
    // ============================================================
    const showToast = (text) => {
        toast.textContent = text;
        toast.showPopover();
        clearTimeout(toastTimer);
        toastTimer = setTimeout(() => toast.hidePopover(), 3000);
    };

    contactForm.addEventListener('submit', (event) => {
        // 静的なサイトなので送信先のサーバーが無い。送信は止めて、通知だけ表示する
        event.preventDefault();

        showError(name, name.value.trim() ? '' : 'お名前を入力してください');
        showError(email, email.value.includes('@') ? '' : 'メールアドレスの形式で入力してください');
        showError(message, message.value.trim().length >= 10 ? '' : 'メッセージは10文字以上で入力してください');

        const firstInvalid = contactForm.querySelector('.invalid');
        if (firstInvalid) {
            firstInvalid.focus();   // 最初にエラーのある欄に移動する
            return;
        }

        showToast(`${name.value.trim()}さん、お問い合わせありがとうございました。（この作例では実際には送信されません）`);
        contactForm.reset();
        updateCount();
    });
}
