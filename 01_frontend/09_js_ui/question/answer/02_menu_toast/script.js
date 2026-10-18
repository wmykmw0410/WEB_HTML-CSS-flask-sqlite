// 解答2：メモカードの「⋯」メニューと、自動で消える通知

const menus = document.querySelectorAll('.menu-popup');
const toast = document.getElementById('toast');
let hideTimer = null;


// TODO 3：通知を表示し、2 秒後に閉じる
const showToast = (message) => {
    toast.textContent = message;
    // すでに開いているときに showPopover() するとエラーになるので、閉じているときだけ開く
    if (!toast.matches(':popover-open')) {
        toast.showPopover();
    }

    // 前のタイマーを取り消さないと、前の操作から2秒後に（早めに）消えてしまう
    clearTimeout(hideTimer);
    hideTimer = setTimeout(() => {
        toast.hidePopover();
    }, 2000);
};


menus.forEach((menu) => {
    // TODO 4：メニューの中のボタン。ボタン1つずつではなく、メニューに1回だけ登録する
    menu.addEventListener('click', (event) => {
        const action = event.target.dataset.action;
        if (!action) {
            return;   // ボタン以外（メニューの余白など）が押されたときは何もしない
        }

        menu.hidePopover();
        const title = menu.closest('.card').querySelector('h2').textContent;

        if (action === 'copy') {
            showToast(`『${title}』をコピーしました`);
        } else if (action === 'delete') {
            showToast(`『${title}』を削除しました`);
        }
    });

    // TODO 5：開閉に合わせて aria-expanded を切り替える
    //         toggle イベントは、ボタン・外側クリック・Esc・hidePopover() のどれで開閉しても発生する
    const opener = document.querySelector(`[popovertarget="${menu.id}"]`);
    menu.addEventListener('toggle', (event) => {
        opener.setAttribute('aria-expanded', event.newState === 'open');
    });
});
