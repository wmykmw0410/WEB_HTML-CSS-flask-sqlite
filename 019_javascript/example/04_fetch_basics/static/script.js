document.querySelectorAll('.like').forEach((button) => {
    button.addEventListener('click', async () => {
        const li = button.closest('li');
        const itemId = li.dataset.id;

        // fetch(URL, {method: ...}) でPOSTリクエストを送る
        const response = await fetch(`/api/items/${itemId}/toggle-like`, {
            method: 'POST',
        });

        // response.json() でレスポンス本文をJSONとして受け取る（Promiseなのでawaitする）
        const data = await response.json();

        // サーバーから返ってきた最新の状態でボタンの表示だけを書き換える
        // ページ全体はリロードされない
        button.textContent = data.liked ? '★' : '☆';
    });
});
