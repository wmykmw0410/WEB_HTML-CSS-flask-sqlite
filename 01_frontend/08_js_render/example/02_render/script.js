// ============================================================
// データから画面を作る
// ============================================================
// 画面（HTML）を直接書き換えるのではなく、「データ（配列）」を正しい状態として持ち、
// 画面は render() で毎回データから作り直す、という考え方

// 1. 画面の元になるデータ
const memos = [
    { id: 1, title: '買い物リスト', category: '家事' },
    { id: 2, title: '企画会議メモ', category: '仕事' },
    { id: 3, title: '読書メモ：銀河鉄道の夜', category: '趣味' },
    { id: 4, title: '資料作成', category: '仕事' },
];

const list = document.getElementById('memo-list');
const searchInput = document.getElementById('search');
const shownCount = document.getElementById('shown-count');

// 2. メモ1件分のカード（li要素）を作って返す
const createCard = (memo) => {
    const li = document.createElement('li');
    li.className = 'card';

    const tag = document.createElement('span');
    tag.className = 'tag';
    tag.textContent = memo.category;

    const title = document.createElement('h2');
    title.textContent = memo.title;   // データは textContent で入れる（06章のXSS）

    li.append(tag, title);
    return li;
};

// 3. 渡された配列から、一覧を作り直す
const render = (items) => {
    list.textContent = '';                  // いったん全部消して
    items.forEach((memo) => {               // データから作り直す
        list.append(createCard(memo));
    });
    shownCount.textContent = `${items.length}件表示中`;
};

// 4. 検索欄に入力するたびに、filter() で絞り込んだ配列を render() に渡す
searchInput.addEventListener('input', () => {
    const matched = memos.filter((memo) => memo.title.includes(searchInput.value));
    render(matched);
});

// 5. 最初に全件を表示する
render(memos);
