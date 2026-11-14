// タブ切り替えの考え方
//   - すべてのタブ（ボタン）から active クラスを外し、パネルを hidden で隠す
//   - 選ばれたタブだけ active クラスを付け、対応するパネルの hidden を外す
//   タブとパネルの対応は、ボタンの data-panel（パネルの id）でたどる

const tabList = document.querySelector('#profile-tabs [role="tablist"]');
const tabs = tabList.querySelectorAll('[role="tab"]');

const selectTab = (selected) => {
    tabs.forEach((tab) => {
        const isSelected = tab === selected;
        tab.classList.toggle('active', isSelected);
        // 選ばれていないタブは Tab キーで飛ばす（タブの間の移動は矢印キーで行うのが一般的）
        tab.tabIndex = isSelected ? 0 : -1;

        const panel = document.getElementById(tab.dataset.panel);
        panel.hidden = !isSelected;   // hidden プロパティに true を入れると隠れる
    });
};

// クリックで切り替える（ボタン1つずつではなく、親の tabList に1回だけ登録する）
tabList.addEventListener('click', (event) => {
    const tab = event.target.closest('[role="tab"]');
    if (tab) {
        selectTab(tab);
    }
});

// ← → キーで隣のタブに移動する
tabList.addEventListener('keydown', (event) => {
    if (event.key !== 'ArrowRight' && event.key !== 'ArrowLeft') {
        return;
    }
    const list = Array.from(tabs);   // NodeList を配列に変換すると indexOf が使える
    const current = list.indexOf(document.activeElement);   // 今フォーカスがある要素
    const step = event.key === 'ArrowRight' ? 1 : -1;
    // % で割った余りを使うと、最後の次は最初に、最初の前は最後に戻る
    const next = list[(current + step + list.length) % list.length];
    selectTab(next);
    next.focus();
});
