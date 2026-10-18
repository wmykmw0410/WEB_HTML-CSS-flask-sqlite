const statusEl = document.getElementById('status');
const list = document.getElementById('memo-list');

// メモ1件分の要素を作る（07_js_dom で学んだ createElement と同じ）
const createMemo = (memo) => {
    const div = document.createElement('div');
    div.className = 'memo';

    const tag = document.createElement('span');
    tag.className = 'tag';
    tag.textContent = memo.category;

    const title = document.createElement('h2');
    title.textContent = memo.title;

    const body = document.createElement('p');
    body.textContent = memo.body;

    div.append(tag, title, body);
    return div;
};


// ============================================================
// fetch() でJSONファイルを読み込んで表示する
// ============================================================
// async を付けた関数の中では await が使える
const loadMemos = async (url) => {
    statusEl.textContent = '読み込み中…';
    statusEl.classList.remove('error');
    list.textContent = '';

    try {
        // 1. fetch(URL) でサーバーにGETリクエストを送り、レスポンスが届くまで await で待つ
        const response = await fetch(url);

        // 2. ステータスコードが200番台でなければ（404 Not Found など）、自分でエラーにする
        //    fetch() は 404 でもエラーにならないので、response.ok の確認が必要
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        // 3. レスポンスの本文をJSONとして読み、JavaScriptの配列に変換する（これも await で待つ）
        const memos = await response.json();

        // 4. 配列から画面を作る
        memos.forEach((memo) => list.append(createMemo(memo)));
        statusEl.textContent = `${memos.length}件読み込みました`;
    } catch (error) {
        // ネットワークの失敗・404・JSONの形式エラーなどは、すべてここに来る
        statusEl.textContent = `読み込みに失敗しました（${error.message}）`;
        statusEl.classList.add('error');
        console.error(error);
    }
};

document.getElementById('load').addEventListener('click', () => {
    loadMemos('data/memos.json');
});

document.getElementById('load-missing').addEventListener('click', () => {
    loadMemos('data/not-found.json');
});


// ============================================================
// 参考：同じ処理を .then() で書くと次のようになる（古いコードでよく使われる書き方）
// ============================================================
// fetch('data/memos.json')
//     .then((response) => response.json())
//     .then((memos) => {
//         memos.forEach((memo) => list.append(createMemo(memo)));
//     })
//     .catch((error) => console.error(error));
