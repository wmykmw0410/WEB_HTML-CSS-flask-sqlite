// 解答1：同じ関数で、ページ内の2つのタブを動かす


// .tabs の要素を1つ受け取り、その中のタブだけを動くようにする関数
const setupTabs = (container) => {
    // container の中だけを探すので、他の .tabs のタブは含まれない
    const tabList = container.querySelector('[role="tablist"]');
    const tabs = Array.from(tabList.querySelectorAll('[role="tab"]'));


    // TODO 1：タブを選ぶ
    const selectTab = (selected) => {
        tabs.forEach((tab) => {
            const isSelected = tab === selected;
            tab.setAttribute('aria-selected', isSelected);
            tab.tabIndex = isSelected ? 0 : -1;

            const panel = document.getElementById(tab.getAttribute('aria-controls'));
            panel.hidden = !isSelected;
        });
    };


    // TODO 2：クリックで切り替える
    tabList.addEventListener('click', (event) => {
        const tab = event.target.closest('[role="tab"]');
        if (tab) {
            selectTab(tab);
        }
    });


    // TODO 3：キーボードで切り替える
    tabList.addEventListener('keydown', (event) => {
        const current = tabs.indexOf(document.activeElement);
        let next;

        if (event.key === 'ArrowRight') {
            next = tabs[(current + 1) % tabs.length];
        } else if (event.key === 'ArrowLeft') {
            next = tabs[(current - 1 + tabs.length) % tabs.length];   // -1 にならないよう length を足してから割る
        } else if (event.key === 'Home') {
            next = tabs[0];
        } else if (event.key === 'End') {
            next = tabs[tabs.length - 1];
        } else {
            return;   // それ以外のキーでは何もしない
        }

        event.preventDefault();   // Home / End でページがスクロールしないようにする
        selectTab(next);
        next.focus();
    });
};


// TODO 4：すべての .tabs に対して呼ぶ。.tabs が3つ・4つに増えても、このままで動く
document.querySelectorAll('.tabs').forEach((container) => {
    setupTabs(container);
});
// forEach(setupTabs) と書いてもよい（関数そのものを渡す）
