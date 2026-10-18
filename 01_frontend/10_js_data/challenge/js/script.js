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
// TODO（2・3・5節）：制作実績を data/works.json から読み込んで表示する（works.html）
//
// 1. createWorkCard(work)：作品1件分の <li class="work-card" data-tags="..."> を作って返す
//    中身は 08_js_render までHTMLに直接書いていたものと同じ：
//      <h2>作品名</h2>
//      <p class="work-date"><time datetime="2026-09">2026年9月</time></p>
//      <p>説明</p>
//      <ul class="tag-list"><li>HTML/CSS</li>…</ul>
//    テキストは必ず textContent で入れる
// 2. loadWorks()：async 関数で data/works.json を fetch し、
//    - 成功したら各作品のカードを #works-list に追加し、#works-status の文字を消す
//    - 失敗したら（response.ok が false、または通信エラー）#works-status に
//      「作品の読み込みに失敗しました。」と表示して error クラスを付ける
// 3. 絞り込み：ステップ3と同じ動きにする。ただしカードは後から作られるので、
//    クリックされた時点で document.querySelectorAll('.work-card') でカードを探す
// ============================================================
const worksList = document.getElementById('works-list');
const filters = document.getElementById('filters');

const createWorkCard = (work) => {
    // TODO
};

const loadWorks = async () => {
    // TODO
};

if (worksList) {
    loadWorks();
    // TODO：絞り込みボタンのイベント
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
