// 解答2：配列のデータからメモカードを作る

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


// TODO 1：メモ1件分のカード要素を作って返す関数
const createCard = (memo) => {
    const li = document.createElement('li');
    li.className = 'card';

    const tag = document.createElement('span');
    tag.className = 'tag';
    tag.textContent = memo.category;
    li.append(tag);

    if (memo.pinned) {
        const pin = document.createElement('span');
        pin.className = 'pin';
        pin.textContent = '📌';
        li.append(pin);
    }

    const title = document.createElement('h2');
    title.textContent = memo.title;   // ユーザーが入力したデータなので textContent で入れる
    li.append(title);

    return li;
};


// TODO 2：渡された配列のメモをすべて表示する関数
const render = (items) => {
    list.textContent = '';                       // いったん空にする
    items.forEach((memo) => {
        list.append(createCard(memo));
    });
    shownCount.textContent = `${items.length}件表示中`;
};


// TODO 3：ピン留めの件数
const pinnedMemos = memos.filter((memo) => memo.pinned);
pinnedCount.textContent = `ピン留め：${pinnedMemos.length}件`;


// TODO 4：タイトル検索
searchInput.addEventListener('input', () => {
    const keyword = searchInput.value;
    const matched = memos.filter((memo) => memo.title.includes(keyword));
    render(matched);
});


// 最初に全件を表示する
render(memos);
