document.addEventListener('DOMContentLoaded', function () {
    const btn = document.getElementById('hamburgerBtn');
    const menu = document.getElementById('hamburgerMenu');
    if (!btn || !menu) {
        return;
    }

    btn.addEventListener('click', function () {
        const willOpen = menu.hidden;
        menu.hidden = !willOpen;
        btn.setAttribute('aria-expanded', String(willOpen));
    });

    // メニューの外側をクリックしたら閉じる（メニュー自身やボタンのクリックは除外）
    document.addEventListener('click', function (event) {
        if (!menu.hidden && !menu.contains(event.target) && event.target !== btn) {
            menu.hidden = true;
            btn.setAttribute('aria-expanded', 'false');
        }
    });
});
