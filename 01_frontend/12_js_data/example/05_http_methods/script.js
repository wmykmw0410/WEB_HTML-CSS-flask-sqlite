// HTTPメソッドを体験する
//
// JSONPlaceholder（https://jsonplaceholder.typicode.com）は、練習用のAPI。
// /posts（投稿）などのデータに対して、メソッドごとに次のような返事をする。
//
//   GET    /posts       投稿の一覧を返す                         → 200 OK
//   GET    /posts/1     1番の投稿を返す（無ければ空の {}）         → 200 OK / 404 Not Found
//   POST   /posts       送った投稿に id: 101 を付けて返す          → 201 Created
//   PUT    /posts/1     送った内容で「丸ごと置き換えた」投稿を返す  → 200 OK
//   PATCH  /posts/1     送った項目だけ「書き換えた」投稿を返す      → 200 OK
//   DELETE /posts/1     空の {} を返す                             → 200 OK
//
// 書き込み系（POST・PUT・PATCH・DELETE）は返事だけで、実際のデータは変わらない。

const BASE_URL = 'https://jsonplaceholder.typicode.com';

const form = document.getElementById('request-form');
const methodSelect = document.getElementById('method');
const pathInput = document.getElementById('path');
const bodyInput = document.getElementById('body');
const sendButton = document.getElementById('send');
const summary = document.getElementById('response-summary');
const responseBody = document.getElementById('response-body');
const historyList = document.getElementById('history');   // history はブラウザの組み込みの名前（window.history）なので避ける

// メソッドごとの、ボディの例
const sampleBodies = {
    POST: { userId: 1, title: '新しい投稿', body: 'POST で追加した本文です' },
    PUT: { id: 1, userId: 1, title: '置き換えたタイトル', body: 'PUT は全体を置き換える' },
    PATCH: { title: 'タイトルだけ変更' },
};


// ============================================================
// メソッドに合わせて、ボディの入力欄を使える・使えないにする
// GET と DELETE は、ふつうボディを送らない
// ============================================================
const updateBodyInput = () => {
    const method = methodSelect.value;
    const hasBody = method === 'POST' || method === 'PUT' || method === 'PATCH';
    bodyInput.disabled = !hasBody;
    if (hasBody && bodyInput.value === '') {
        bodyInput.value = JSON.stringify(sampleBodies[method], null, 2);
    }
};

methodSelect.addEventListener('change', () => {
    bodyInput.value = '';   // メソッドを変えたら、そのメソッドの例に入れ替える
    updateBodyInput();
});


// ============================================================
// 例のボタン：メソッド・パス・ボディをまとめて設定する
// ============================================================
document.getElementById('presets').addEventListener('click', (event) => {
    const button = event.target.closest('button');
    if (!button) {
        return;
    }
    methodSelect.value = button.dataset.method;
    pathInput.value = button.dataset.path;
    bodyInput.value = '';
    updateBodyInput();
});


// ============================================================
// 送信：fetch() の2つ目の引数で、メソッド・ヘッダー・ボディを指定する
// ============================================================
form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const method = methodSelect.value;
    const url = BASE_URL + pathInput.value.trim();
    const options = { method };

    if (!bodyInput.disabled) {
        // 送る前に、ボディが正しいJSONかを確かめる（1節：JSON.parse は間違ったJSONでエラーになる）
        try {
            JSON.parse(bodyInput.value);
        } catch (error) {
            summary.textContent = `ボディが正しいJSONではありません：${error.message}`;
            summary.className = 'status error';
            return;
        }
        options.headers = { 'Content-Type': 'application/json' };   // 「ボディはJSONです」と伝える
        options.body = bodyInput.value;                              // 送るのは文字列
    }

    sendButton.disabled = true;
    summary.textContent = '送信中…';
    summary.className = '';
    responseBody.textContent = '';
    const startedAt = performance.now();

    try {
        const response = await fetch(url, options);
        const ms = Math.round(performance.now() - startedAt);

        // 404 などでも fetch() はエラーにならない。response.status と response.ok で結果を見る（3節）
        const data = await response.json();
        summary.textContent = `${response.status} ${response.ok ? '成功' : '失敗'}（${ms}ミリ秒）`;
        summary.className = `status ${response.ok ? 'ok' : 'error'}`;
        responseBody.textContent = JSON.stringify(data, null, 2);   // 見やすく字下げして表示する

        addHistory(method, pathInput.value.trim(), response.status, response.ok);
    } catch (error) {
        // インターネットにつながっていないときなど、通信そのものが失敗したとき
        summary.textContent = `通信に失敗しました：${error.message}`;
        summary.className = 'status error';
    } finally {
        sendButton.disabled = false;
    }
});


// ============================================================
// 履歴に1行追加する（新しいものを上に）
// ============================================================
const addHistory = (method, path, status, ok) => {
    const li = document.createElement('li');

    const methodLabel = document.createElement('span');
    methodLabel.className = `method ${method}`;
    methodLabel.textContent = method;

    const pathText = document.createElement('span');
    pathText.textContent = path;

    const statusText = document.createElement('span');
    statusText.className = `status ${ok ? 'ok' : 'error'}`;
    statusText.textContent = status;

    li.append(methodLabel, pathText, statusText);
    historyList.prepend(li);
};


updateBodyInput();
