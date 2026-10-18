// 解答5：JSONPlaceholder を相手に、GET・POST・PATCH・DELETE で投稿ボードを作る

const BASE_URL = 'https://jsonplaceholder.typicode.com';

const form = document.getElementById('add-form');
const titleInput = document.getElementById('new-title');
const bodyInput = document.getElementById('new-body');
const log = document.getElementById('log');
const list = document.getElementById('post-list');

let posts = [];   // 画面の元になるデータ（5節と同じく、データを変えてから render() する）


// TODO 1：リクエストを送る関数。メソッドが違っても、送り方はこの1つにまとめる
const request = async (method, path, data) => {
    const options = { method };
    if (data) {
        options.headers = { 'Content-Type': 'application/json' };
        options.body = JSON.stringify(data);   // オブジェクトはそのまま送れないので文字列にする
    }

    const response = await fetch(BASE_URL + path, options);
    log.textContent = `${method} ${path} → ${response.status}`;
    log.classList.toggle('error', !response.ok);

    if (!response.ok) {
        throw new Error(`${response.status}`);   // 404 などは自分でエラーにする（3節）
    }
    return response.json();
};


// TODO 2：投稿1件分の li
const createItem = (post) => {
    const li = document.createElement('li');
    li.dataset.id = post.id;

    const text = document.createElement('div');
    text.className = 'text';
    const title = document.createElement('h2');
    title.textContent = post.title;
    const body = document.createElement('p');
    body.textContent = post.body;
    text.append(title, body);

    const done = document.createElement('button');
    done.type = 'button';
    done.className = 'done';
    done.textContent = '済にする';
    done.disabled = post.title.startsWith('【済】');   // すでに済なら押せない

    const remove = document.createElement('button');
    remove.type = 'button';
    remove.className = 'remove';
    remove.textContent = '削除';

    li.append(text, done, remove);
    return li;
};


// TODO 3：データから画面を作り直す
const render = () => {
    list.textContent = '';
    posts.forEach((post) => list.append(createItem(post)));
};


// TODO 4：最初の一覧を GET で読み込む
const loadPosts = async () => {
    try {
        posts = await request('GET', '/posts?userId=1&_limit=5');
        render();
    } catch (error) {
        log.textContent = `一覧を読み込めませんでした（${error.message}）`;
        log.classList.add('error');
    }
};


// TODO 5：POST で投稿する
form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const title = titleInput.value.trim();
    if (!title) {
        return;
    }

    try {
        const created = await request('POST', '/posts', { userId: 1, title, body: bodyInput.value.trim() });
        // JSONPlaceholder は毎回 id: 101 を返すので、一覧で区別できるよう id を付け直す
        created.id = Date.now();
        posts.unshift(created);   // 新しい投稿を先頭に
        render();
        form.reset();
    } catch (error) {
        log.textContent = `投稿できませんでした（${error.message}）`;
    }
});


// TODO 6：済にする（PATCH）・削除（DELETE）。作り直される li ではなく、親の list に1回だけ登録する
list.addEventListener('click', async (event) => {
    const li = event.target.closest('li');
    if (!li) {
        return;
    }
    const id = Number(li.dataset.id);
    const post = posts.find((p) => p.id === id);

    try {
        if (event.target.classList.contains('done')) {
            const newTitle = `【済】${post.title}`;
            await request('PATCH', `/posts/${id}`, { title: newTitle });   // 変える項目だけを送る
            post.title = newTitle;
        } else if (event.target.classList.contains('remove')) {
            await request('DELETE', `/posts/${id}`);                       // DELETE はボディを送らない
            posts = posts.filter((p) => p.id !== id);
        } else {
            return;
        }
        render();
    } catch (error) {
        // 失敗したときはデータを変えない（画面もそのまま）
    }
});


// TODO 7：存在しない投稿を読み込むと 404 になる
document.getElementById('load-missing').addEventListener('click', async () => {
    try {
        await request('GET', '/posts/9999');
    } catch (error) {
        log.textContent += '：投稿が見つかりませんでした';
    }
});


loadPosts();
