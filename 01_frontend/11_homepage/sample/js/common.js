/*
common.js：全ページ共通の動き

    1. 表示設定（テーマ）       … ポップアップ（09_js_ui 2節）＋ localStorage（10_js_data 4節）
    2. ハンバーガーメニュー     … 06_js_events 1節・08_js_render の制作課題ステップ3
    3. ツールチップ             … ホバーとフォーカス（06_js_events 3節）
    4. スクロールに応じた表示   … scroll イベント（09_js_ui 5節）
    5. ふわっと表示             … IntersectionObserver（09_js_ui 5節）

ページによっては対象の要素が無いので、if (要素) で存在を確認してから使う。
*/

// ============================================================
// 1. 表示設定（テーマ）：選んだテーマを localStorage に保存し、<html data-theme="..."> に反映する
//    CSS では :root[data-theme="dark"] のときだけ色の変数を差し替えている
// ============================================================
const THEME_KEY = 'portfolio.theme';

const applyTheme = (theme) => {
    if (theme === 'auto') {
        document.documentElement.removeAttribute('data-theme');   // OSの設定（prefers-color-scheme）に任せる
    } else {
        document.documentElement.setAttribute('data-theme', theme);
    }
};

const savedTheme = localStorage.getItem(THEME_KEY) ?? 'auto';
applyTheme(savedTheme);

const settings = document.getElementById('settings');
if (settings) {
    // 保存されている値のラジオボタンにチェックを付ける
    const current = settings.querySelector(`input[value="${savedTheme}"]`);
    if (current) {
        current.checked = true;
    }

    // ラジオボタンが変わったら、保存して反映する（親の settings に1回だけ登録）
    settings.addEventListener('change', (event) => {
        const theme = event.target.value;
        localStorage.setItem(THEME_KEY, theme);
        applyTheme(theme);
    });
}


// ============================================================
// 2. ハンバーガーメニュー
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
// 3. ツールチップ：data-tip を持つ要素に、マウスを乗せる・フォーカスすると説明を出す
// ============================================================
document.querySelectorAll('[data-tip]').forEach((el) => {
    const tip = document.createElement('span');
    tip.className = 'tooltip';
    tip.textContent = el.dataset.tip;
    tip.hidden = true;
    el.append(tip);

    const show = () => { tip.hidden = false; };
    const hide = () => { tip.hidden = true; };
    el.addEventListener('mouseenter', show);
    el.addEventListener('mouseleave', hide);
    el.addEventListener('focus', show);
    el.addEventListener('blur', hide);
});


// ============================================================
// 4. スクロールに応じた表示：ヘッダーの影・読んだ量のバー・トップへ戻るボタン
// ============================================================
const header = document.getElementById('site-header');
const progress = document.getElementById('progress');
const toTop = document.getElementById('to-top');

const onScroll = () => {
    const y = window.scrollY;
    header.classList.toggle('scrolled', y > 10);
    toTop.hidden = y < 300;

    const max = document.documentElement.scrollHeight - window.innerHeight;
    progress.style.width = `${max > 0 ? (y / max) * 100 : 0}%`;
};

window.addEventListener('scroll', onScroll);
onScroll();

toTop.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});


// ============================================================
// 5. ふわっと表示：.fade-in の要素が画面に入ったら visible クラスを付ける
//    ページごとのファイル（works.js など）で後から作った要素も対象にできるよう、関数にしておく
// ============================================================
const fadeObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            fadeObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.15 });

const observeFadeIn = (root = document) => {
    root.querySelectorAll('.fade-in:not(.visible)').forEach((el) => fadeObserver.observe(el));
};

observeFadeIn();
