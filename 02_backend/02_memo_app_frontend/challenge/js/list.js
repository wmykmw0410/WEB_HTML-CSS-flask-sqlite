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
    // TODO
    return list;   // ステップ3を書くまでは、並べ替えずにそのまま返す
};

const getVisibleMemos = () => {
    // TODO
    return memos;   // ステップ3を書くまでは、全件をそのまま返す
};


// ============================================================
// ステップ2：状態から画面を作り直す
// ============================================================
const render = () => {
    // TODO
};


// ============================================================
// ステップ3：絞り込みボタンと検索欄
// ============================================================
const selectCategory = (category) => {
    // TODO
    render();
};

// TODO：絞り込みボタン（#filters の click）


// TODO：検索欄（#keyword の input）



// ============================================================
// ステップ6：ピン留めと削除（カードは render() のたびに作り直されるので、親の #memo-list に登録する）
// ============================================================
// TODO：#memo-list の click で、★（.pin-button）と削除（.delete-button）を処理する



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

    // ステップ3：前回選んだカテゴリを復元する
    // TODO：下の行を、保存したカテゴリ（そのボタンがあるときだけ）を選ぶように書き換える
    selectCategory('all');   // selectCategory() の中で render() される
};

start();
