/*
common.js：全ページ共通の処理（完成済み）

02_backend/100_memo_api の static/script.js と同じ書き方。
    - showToast(message, isError)：右下に出て3秒で消える通知
    - openConfirm(message, onOk)：確認ダイアログ。「OK」が押されたら onOk を呼ぶ
    - ハンバーガーメニュー・配色の切り替え・ヘッダーの影・トップへ戻るボタン
    - observeFadeIn(elements)：画面に入ったらふわっと表示する
*/


// ============================================================
// 自動で消える通知（01_frontend/09_js_ui 2節）
// ============================================================
const toast = document.getElementById('toast');
let toastTimer = null;

const showToast = (message, isError = false) => {
    toast.textContent = message;
    toast.classList.toggle('error', isError);
    // すでに開いているときに showPopover() するとエラーになるので、閉じているときだけ開く
    if (!toast.matches(':popover-open')) {
        toast.showPopover();
    }
    // 連続で呼ばれたら、前のタイマーを取り消して、そこから数え直す
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
        toast.hidePopover();
    }, 3000);
};


// ============================================================
// 確認ダイアログ（01_frontend/09_js_ui 3節）
// confirm() の代わりに使う。「OK」が押されたときに呼んでほしい処理を、コールバック関数で渡す
// （01_frontend/05_js_basics 2節）
//   openConfirm('削除しますか？', () => { ...OK のときの処理... });
// ============================================================
const confirmDialog = document.getElementById('confirm-dialog');
let onConfirm = null;   // OK が押されたときに呼ぶ関数

const openConfirm = (message, onOk) => {
    document.getElementById('confirm-message').textContent = message;
    onConfirm = onOk;
    confirmDialog.showModal();
};

document.getElementById('confirm-ok').addEventListener('click', () => {
    confirmDialog.close();
    onConfirm();
});

document.getElementById('confirm-cancel').addEventListener('click', () => {
    confirmDialog.close();
});

// 暗い背景（dialog 自身）をクリックしたら閉じる。Esc キーではブラウザが閉じてくれる
confirmDialog.addEventListener('click', (event) => {
    if (event.target === confirmDialog) {
        confirmDialog.close();
    }
});


// ============================================================
// ハンバーガーメニュー（01_frontend/08_js_render の制作課題）
// ============================================================
const navToggle = document.getElementById('nav-toggle');
const navLinks = document.getElementById('nav-links');

navToggle.addEventListener('click', () => {
    const isOpen = navLinks.classList.toggle('open');
    navToggle.setAttribute('aria-expanded', isOpen);
    navToggle.setAttribute('aria-label', isOpen ? 'メニューを閉じる' : 'メニューを開く');
});


// ============================================================
// 配色の切り替え（01_frontend/10_js_data 4節の「応用」）
// 読み込み直後の反映は、各ページの <head> の中で行っている
// ============================================================
const themeButton = document.getElementById('theme-toggle');
const root = document.documentElement;

// 今の配色：ボタンで選んだもの（data-theme）が無ければ、OS の設定に従う
const currentTheme = () => {
    if (root.dataset.theme) {
        return root.dataset.theme;
    }
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
};

const updateThemeLabel = () => {
    const next = currentTheme() === 'dark' ? 'ライト' : 'ダーク';
    themeButton.setAttribute('aria-label', `${next}モードに切り替える`);
    themeButton.title = `${next}モードに切り替える`;
};

themeButton.addEventListener('click', () => {
    const next = currentTheme() === 'dark' ? 'light' : 'dark';
    root.dataset.theme = next;
    saveSetting('theme', next);   // storage.js
    updateThemeLabel();
});

updateThemeLabel();


// ============================================================
// スクロール（01_frontend/09_js_ui 5節）
//   - 少しスクロールしたらヘッダーに影
//   - 300px 以上スクロールしたら「トップへ戻る」ボタン
// ============================================================
const siteHeader = document.querySelector('.site-header');
const toTop = document.getElementById('to-top');

const onScroll = () => {
    const y = window.scrollY;
    siteHeader.classList.toggle('scrolled', y > 10);
    toTop.hidden = y < 300;
};
window.addEventListener('scroll', onScroll);
onScroll();

toTop.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});


// ============================================================
// 画面に入ったらふわっと表示する（01_frontend/09_js_ui 5節）
// list.js の render() でカードを作るたびに呼ぶ
// ============================================================
const fadeInObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            fadeInObserver.unobserve(entry.target);   // 一度表示したら、もう監視しない
        }
    });
}, { threshold: 0.1 });

// fade-in クラス（最初は透明）は、HTML ではなくここで付ける（JavaScript が動かないときに透明のまま残らないように）
const observeFadeIn = (elements) => {
    elements.forEach((el) => {
        el.classList.add('fade-in');
        fadeInObserver.observe(el);
    });
};
