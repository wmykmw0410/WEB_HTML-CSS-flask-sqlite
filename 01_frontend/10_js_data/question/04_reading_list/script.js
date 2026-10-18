const STORAGE_KEY = 'reading-list';

const form = document.getElementById('add-form');
const titleInput = document.getElementById('new-title');
const authorInput = document.getElementById('new-author');
const filterButtons = document.querySelectorAll('.filters button');
const summary = document.getElementById('summary');
const list = document.getElementById('book-list');


// TODO 1
const load = () => {
};

const save = () => {
};


let books = load();        // 画面の元になるデータ（保存する）
let filter = 'all';        // 今の表示の切り替え（'all' / 'unread' / 'read'）。保存しない


// TODO 2
const createItem = (book) => {
};


// TODO 3
const render = () => {
};


// TODO 4


// TODO 5


// TODO 6


render();
