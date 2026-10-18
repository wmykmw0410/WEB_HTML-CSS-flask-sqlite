/*
山田太郎のポートフォリオサイト 共通スクリプト（全ページで読み込む）
ページによって対象の要素が無いので、if (要素) で存在を確認してから使う。
*/

// ============================================================
// ハンバーガーメニュー（全ページ）
// ============================================================
const navToggle = document.getElementById('nav-toggle');
if (navToggle) {
    const navLinks = document.getElementById('nav-links');

    navToggle.addEventListener('click', () => {
        const isOpen = navLinks.classList.toggle('open');
        navToggle.setAttribute('aria-expanded', isOpen);
    });
}

// ============================================================
// 制作実績の絞り込み（works.html）
// ============================================================
const filters = document.getElementById('filters');
if (filters) {
    filters.addEventListener('click', (event) => {
        const button = event.target.closest('button');
        if (!button) {
            return;
        }

        filters.querySelectorAll('button').forEach((b) => b.classList.remove('active'));
        button.classList.add('active');

        const selected = button.dataset.tag;
        document.querySelectorAll('.work-card').forEach((card) => {
            const tags = card.dataset.tags.split(' ');
            const match = selected === 'all' || tags.includes(selected);
            card.classList.toggle('hidden', !match);
        });
    });
}

// ============================================================
// お問い合わせフォームの入力チェック（contact.html）
// ============================================================
const contactForm = document.getElementById('contact-form');
if (contactForm) {
    const result = document.getElementById('contact-result');

    // エラーメッセージの表示・非表示を切り替える
    const showError = (input, message) => {
        document.getElementById(`${input.id}-error`).textContent = message;
        input.classList.toggle('invalid', message !== '');
    };

    contactForm.addEventListener('submit', (event) => {
        // このサイトは静的なページなので、送信先のサーバーが無い。送信は止めてメッセージだけ表示する
        event.preventDefault();

        const name = document.getElementById('name');
        const email = document.getElementById('email');
        const message = document.getElementById('message');

        showError(name, name.value.trim() ? '' : 'お名前を入力してください');
        showError(email, email.value.includes('@') ? '' : 'メールアドレスの形式で入力してください');
        showError(message, message.value.trim().length >= 10 ? '' : 'メッセージは10文字以上で入力してください');

        if (contactForm.querySelector('.invalid')) {
            result.textContent = '';
            return;
        }

        result.textContent = `${name.value.trim()}さん、お問い合わせありがとうございました。（この作例では実際には送信されません）`;
        contactForm.reset();
    });
}
