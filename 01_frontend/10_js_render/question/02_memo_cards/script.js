const memos = [
    { id: 1, title: '買い物リスト', category: '家事', pinned: true },
    { id: 2, title: '企画会議メモ', category: '仕事', pinned: false },
    { id: 3, title: '読書メモ：銀河鉄道の夜', category: '趣味', pinned: false },
    { id: 4, title: 'アプリのアイデア', category: 'アイデア', pinned: true },
    { id: 5, title: '旅行の持ち物リスト', category: 'プライベート', pinned: false },
];

const list = document.getElementById('memo-list');
const searchInput = document.getElementById('search');
const pinnedCount = document.getElementById('pinned-count');
const shownCount = document.getElementById('shown-count');


// TODO 1
const createCard = (memo) => {
};


// TODO 2
const render = (items) => {
};


// TODO 3


// TODO 4


// 最初に全件を表示する
render(memos);
