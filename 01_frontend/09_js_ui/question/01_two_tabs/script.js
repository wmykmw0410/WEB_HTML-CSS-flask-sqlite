// ============================================================
// .tabs の要素を1つ受け取り、その中のタブだけを動くようにする関数
// ============================================================
const setupTabs = (container) => {
    // ポイント：document.querySelectorAll ではなく container.querySelectorAll で探すと、
    //          「この .tabs の中のタブ」だけが取り出せる
    const tabList = container.querySelector('[role="tablist"]');
    const tabs = Array.from(tabList.querySelectorAll('[role="tab"]'));   // 配列にしておくと indexOf が使える


    // TODO 1
    const selectTab = (selected) => {
    };


    // TODO 2


    // TODO 3
};


// TODO 4
