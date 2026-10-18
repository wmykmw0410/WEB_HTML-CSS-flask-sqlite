// 解答2：JSONファイルから本の一覧を読み込んで、表にする

const statusEl = document.getElementById('status');
const rows = document.getElementById('book-rows');
const summary = document.getElementById('summary');


// TODO 1：本1冊分の行を作る
const createRow = (book) => {
    const tr = document.createElement('tr');
    [book.title, book.author, book.year, book.read ? '✓' : ''].forEach((value) => {
        const td = document.createElement('td');
        td.textContent = value;
        tr.append(td);
    });
    return tr;
};


// TODO 2：読み込んで表示する
const loadBooks = async () => {
    try {
        const response = await fetch('data/books.json');
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        const books = await response.json();

        books.forEach((book) => rows.append(createRow(book)));

        const readCount = books.filter((book) => book.read).length;
        statusEl.textContent = '';
        summary.textContent = `${books.length}冊中${readCount}冊読了`;
    } catch (error) {
        statusEl.textContent = '本の一覧を読み込めませんでした';
        statusEl.classList.add('error');
        console.error(error);
    }
};

loadBooks();
