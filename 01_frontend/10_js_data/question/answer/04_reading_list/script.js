// 解答4：「データ → 保存 → 描画」の考え方で作る読書記録アプリ

const STORAGE_KEY = 'reading-list';

const form = document.getElementById('add-form');
const titleInput = document.getElementById('new-title');
const authorInput = document.getElementById('new-author');
const filterButtons = document.querySelectorAll('.filters button');
const summary = document.getElementById('summary');
const list = document.getElementById('book-list');


// TODO 1：読み込みと保存。localStorage には文字列しか保存できないので JSON に変換する
const load = () => {
    const json = localStorage.getItem(STORAGE_KEY);
    return json ? JSON.parse(json) : [];
};

const save = () => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(books));
};


let books = load();        // 画面の元になるデータ（保存する）
let filter = 'all';        // 今の表示の切り替え（'all' / 'unread' / 'read'）。保存しない


// TODO 2：本1冊分の li
const createItem = (book) => {
    const li = document.createElement('li');
    li.dataset.id = book.id;
    li.classList.toggle('read', book.read);

    const info = document.createElement('div');
    info.className = 'info';

    const title = document.createElement('span');
    title.className = 'title';
    title.textContent = book.title;

    const author = document.createElement('span');
    author.className = 'author';
    author.textContent = book.author;

    info.append(title, document.createElement('br'), author);

    const toggle = document.createElement('button');
    toggle.type = 'button';
    toggle.className = 'toggle';
    toggle.textContent = book.read ? '未読に戻す' : '読了にする';

    const remove = document.createElement('button');
    remove.type = 'button';
    remove.className = 'remove';
    remove.textContent = '削除';

    li.append(info, toggle, remove);
    return li;
};


// TODO 3：データから画面を作り直す
const render = () => {
    list.textContent = '';

    // 表示の切り替えは books を変えずに、「表示する分」を別の配列として選ぶ
    const visible = books.filter((book) => {
        if (filter === 'unread') {
            return !book.read;
        }
        if (filter === 'read') {
            return book.read;
        }
        return true;
    });

    visible.forEach((book) => {
        list.append(createItem(book));
    });

    const readCount = books.filter((book) => book.read).length;
    summary.textContent = `全${books.length}冊（読了 ${readCount}冊）`;
};


// TODO 4：追加。データを変える → 保存 → 描画
form.addEventListener('submit', (event) => {
    event.preventDefault();
    const title = titleInput.value.trim();
    if (!title) {
        return;
    }
    const author = authorInput.value.trim() || '著者不明';   // 空文字は falsy なので、右側の値になる

    books.push({ id: Date.now(), title, author, read: false });
    save();
    render();

    form.reset();          // 入力欄を空にする
    titleInput.focus();    // 続けて入力しやすいように、タイトル欄に戻る
});


// TODO 5：読了の切り替えと削除。作り直されない親の list に1回だけ登録する
list.addEventListener('click', (event) => {
    const li = event.target.closest('li');
    if (!li) {
        return;
    }
    const id = Number(li.dataset.id);   // dataset の値は文字列なので数値に戻す
    const book = books.find((b) => b.id === id);

    if (event.target.classList.contains('toggle')) {
        book.read = !book.read;
    } else if (event.target.classList.contains('remove')) {
        if (!confirm(`『${book.title}』を削除しますか？`)) {
            return;   // キャンセルなら何も変えない
        }
        books = books.filter((b) => b.id !== id);
    } else {
        return;       // ボタン以外の場所が押されたときは何もしない
    }

    save();
    render();
});


// TODO 6：表示の切り替え。データは変わらないので save() はしない
filterButtons.forEach((button) => {
    button.addEventListener('click', () => {
        filterButtons.forEach((b) => b.setAttribute('aria-pressed', 'false'));
        button.setAttribute('aria-pressed', 'true');

        filter = button.dataset.filter;
        render();
    });
});


render();
