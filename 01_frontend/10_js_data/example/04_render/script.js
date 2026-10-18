// 「データ → 画面」の考え方
//
//   データ（todos 配列）が「正しい状態」を持ち、画面は render() でデータから作り直す。
//   ボタンが押されたら、画面を直接いじるのではなく
//     1. データを変更する
//     2. 保存する（save）
//     3. 画面を作り直す（render）
//   の3つを必ずこの順で行う。こうすると「データと画面がずれる」バグが起きにくい。

const STORAGE_KEY = 'todos';

// ---------- データの読み込みと保存 ----------
const load = () => {
    const json = localStorage.getItem(STORAGE_KEY);
    return json ? JSON.parse(json) : [];
};

const save = () => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(todos));
};

let todos = load();   // 画面の元になるデータ（状態）


// ---------- データから画面を作る ----------
const list = document.getElementById('todo-list');
const summary = document.getElementById('summary');

const render = () => {
    list.textContent = '';   // いったん全部消して、データから作り直す

    todos.forEach((todo) => {
        const li = document.createElement('li');
        li.classList.toggle('done', todo.done);
        li.dataset.id = todo.id;

        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.checked = todo.done;
        checkbox.className = 'toggle';

        const title = document.createElement('span');
        title.textContent = todo.title;

        const remove = document.createElement('button');
        remove.type = 'button';
        remove.textContent = '削除';
        remove.className = 'remove';

        li.append(checkbox, title, remove);
        list.append(li);
    });

    const left = todos.filter((todo) => !todo.done).length;
    summary.textContent = `全${todos.length}件（未完了 ${left}件）`;
};


// ---------- 操作：データを変える → 保存 → 描画 ----------
document.getElementById('add-form').addEventListener('submit', (event) => {
    event.preventDefault();
    const input = document.getElementById('new-title');
    const title = input.value.trim();
    if (!title) {
        return;
    }

    todos.push({ id: Date.now(), title, done: false });   // Date.now()：現在時刻のミリ秒。簡易的なIDとして使う
    save();
    render();
    input.value = '';
});

// ボタンやチェックボックスは render() のたびに作り直されるので、
// 個々の要素ではなく、変わらない親（#todo-list）にイベントを登録する
list.addEventListener('click', (event) => {
    const li = event.target.closest('li');
    if (!li) {
        return;
    }
    const id = Number(li.dataset.id);   // dataset の値は文字列なので数値に戻す

    if (event.target.classList.contains('toggle')) {
        const todo = todos.find((t) => t.id === id);
        todo.done = !todo.done;
    } else if (event.target.classList.contains('remove')) {
        todos = todos.filter((t) => t.id !== id);
    } else {
        return;
    }
    save();
    render();
});

render();
