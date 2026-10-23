/*
list.js：メモ一覧ページ（index.html）の処理

「データ → 画面」の考え方（01_frontend/10_js_data 5節）で作る。
    - memos：全メモの配列（storage.js で読み込み・保存する）
    - selectedCategory・keyword：今の絞り込み・検索の条件
画面は render() で、これらの「状態」から毎回作り直す。
ボタンが押されたら「状態を変える → （データを変えたときは）保存 → render()」の順に処理する。
*/

const memoList = document.getElementById('memo-list');
const listCount = document.getElementById('list-count');
const emptyMessage = document.getElementById('empty');
const filters = document.getElementById('filters');
const keywordInput = document.getElementById('keyword');

const FILTER_KEY = 'memo-app.filter';   // 選んだカテゴリを覚えておくキー

let memos = [];                 // 全メモ
let selectedCategory = 'all';   // 選択中のカテゴリ
let keyword = '';               // 検索キーワード


// ============================================================
// メモ1件分のカードを作る（完成済み）
// 作る構造は 02_backend/100_memo_api の templates/memos/index.html と同じ
// ============================================================
const createCard = (memo) => {
    const card = document.createElement('article');
    card.className = 'card';
    card.dataset.id = memo.id;

    const pin = document.createElement('button');
    pin.type = 'button';
    pin.className = 'pin-button';
    pin.textContent = memo.is_pinned ? '★' : '☆';

    const link = document.createElement('a');
    link.className = 'card-link';
    link.href = `detail.html?id=${memo.id}`;   // どのメモかを、URL の ?id= で詳細ページに伝える

    const tag = document.createElement('span');
    tag.className = 'tag';
    tag.textContent = memo.category;

    const title = document.createElement('h2');
    title.className = 'card-title';
    title.textContent = memo.title;

    const body = document.createElement('p');
    body.className = 'card-body';
    body.textContent = memo.body;

    link.append(tag, title, body);

    if (memo.due_date) {
        const due = document.createElement('p');
        due.className = 'card-due';
        const time = document.createElement('time');
        time.dateTime = memo.due_date;          // <time datetime="2026-10-07">
        time.textContent = memo.due_date;
        due.append('期限：', time);
        link.append(due);
    }

    const actions = document.createElement('div');
    actions.className = 'memo-actions';

    const edit = document.createElement('a');
    edit.href = `edit.html?id=${memo.id}`;
    edit.textContent = '編集';

    const remove = document.createElement('button');
    remove.type = 'button';
    remove.className = 'button-danger delete-button';
    remove.textContent = '削除';

    actions.append(edit, remove);
    card.append(pin, link, actions);
    return card;
};


// ============================================================
// ステップ3：並び替え・絞り込み・検索をして、表示するメモを決める
// ============================================================

// ピン留めを先頭に、それ以外は新しい順（id が大きい順）に並べた「新しい配列」を返す
// （02_backend/100_memo_api の一覧と同じ並び順）
const sortMemos = (list) => {
    // sort() は元の配列を並べ替えてしまうので、slice() でコピーしてから並べ替える
    return list.slice().sort((a, b) => {
        if (a.is_pinned !== b.is_pinned) {
            return a.is_pinned ? -1 : 1;   // マイナスなら a が前、プラスなら b が前
        }
        return b.id - a.id;                // id が大きい（新しい）方が前
    });
};

const getVisibleMemos = () => {
    return sortMemos(memos).filter((memo) => {
        const matchCategory = selectedCategory === 'all' || memo.category === selectedCategory;
        const matchKeyword = memo.title.includes(keyword) || memo.body.includes(keyword);
        return matchCategory && matchKeyword;
    });
};


// ============================================================
// ステップ2：状態から画面を作り直す
// ============================================================
const render = () => {
    const visible = getVisibleMemos();

    memoList.textContent = '';
    visible.forEach((memo) => memoList.append(createCard(memo)));
    observeFadeIn(memoList.querySelectorAll('.card'));   // common.js：ふわっと表示

    emptyMessage.hidden = visible.length > 0;
    emptyMessage.textContent = memos.length === 0
        ? 'メモはまだありません。「メモを追加」から追加しましょう。'
        : '該当するメモはありません';

    listCount.textContent = `${memos.length}件中 ${visible.length}件を表示`;
};


// ============================================================
// ステップ3：絞り込みボタンと検索欄
// ============================================================
const selectCategory = (category) => {
    selectedCategory = category;
    filters.querySelectorAll('button').forEach((button) => {
        button.classList.toggle('active', button.dataset.category === category);
    });
    render();
};

filters.addEventListener('click', (event) => {
    const button = event.target.closest('button');
    if (!button) {
        return;
    }
    selectCategory(button.dataset.category);
    saveSetting(FILTER_KEY, button.dataset.category);   // 次に開いたときのために覚えておく（storage.js）
});

keywordInput.addEventListener('input', () => {
    keyword = keywordInput.value.trim();   // 状態を変える
    render();                              // 状態から作り直す
});


// ============================================================
// ステップ6：ピン留めと削除（カードは render() のたびに作り直されるので、親の #memo-list に登録する）
// ============================================================
memoList.addEventListener('click', (event) => {
    const card = event.target.closest('.card');
    if (!card) {
        return;
    }
    const id = Number(card.dataset.id);   // dataset の値は文字列なので数値に戻す
    const memo = memos.find((m) => m.id === id);

    if (event.target.classList.contains('pin-button')) {
        memo.is_pinned = !memo.is_pinned;
        saveMemos(memos);
        render();
        showToast(memo.is_pinned ? 'ピン留めしました' : 'ピン留めを外しました');   // common.js
    } else if (event.target.classList.contains('delete-button')) {
        openConfirm(`「${memo.title}」を削除しますか？`, () => {   // common.js：OK のときだけ呼ばれる
            memos = memos.filter((m) => m.id !== id);
            saveMemos(memos);
            render();
            showToast('メモを削除しました');
        });
    }
});


// ============================================================
// データを初期状態に戻す（完成済み）
// ============================================================
document.getElementById('reset').addEventListener('click', () => {
    openConfirm('追加・編集したメモがすべて消え、初期データに戻ります。よろしいですか？', () => {
        resetMemos();
        location.reload();
    });
});


// ============================================================
// ページを開いたときの処理
// ============================================================
const start = async () => {
    try {
        memos = await initMemos();
    } catch (error) {
        console.error(error);
        listCount.textContent = 'メモを読み込めませんでした。python -m http.server で起動して開いているか確認してください。';
        return;
    }

    // ステップ3：前回選んだカテゴリを復元する（そのカテゴリのボタンがあるときだけ）
    const saved = loadSetting(FILTER_KEY);
    const savedButton = saved ? filters.querySelector(`button[data-category="${saved}"]`) : null;
    selectCategory(savedButton ? saved : 'all');   // selectCategory() の中で render() される
};

start();
