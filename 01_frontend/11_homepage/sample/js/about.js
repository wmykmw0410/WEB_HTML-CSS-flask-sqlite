/*
about.js：プロフィール（about.html）の動き

    タブ切り替え … 09_js_ui 1節
    （技術名のツールチップは common.js の data-tip の仕組みで表示している）
*/

const tabList = document.querySelector('#profile-tabs [role="tablist"]');

if (tabList) {
    const tabs = Array.from(tabList.querySelectorAll('[role="tab"]'));

    const selectTab = (selected) => {
        tabs.forEach((tab) => {
            const isSelected = tab === selected;
            tab.classList.toggle('active', isSelected);
            tab.tabIndex = isSelected ? 0 : -1;
            document.getElementById(tab.dataset.panel).hidden = !isSelected;
        });
    };

    tabList.addEventListener('click', (event) => {
        const tab = event.target.closest('[role="tab"]');
        if (tab) {
            selectTab(tab);
        }
    });

    // ← → キーで隣のタブへ
    tabList.addEventListener('keydown', (event) => {
        if (event.key !== 'ArrowRight' && event.key !== 'ArrowLeft') {
            return;
        }
        const step = event.key === 'ArrowRight' ? 1 : -1;
        const index = tabs.indexOf(document.activeElement);
        const next = tabs[(index + step + tabs.length) % tabs.length];
        selectTab(next);
        next.focus();
    });
}
