/*
works.js：制作実績（works.html）の動き

    1. 一覧の表示   … data/works.json を fetch して（10_js_data 2・3節）、カードを作る（10_js_data 5節）
    2. 絞り込み     … 08_js_render 3節
    3. 詳細の表示   … モーダルウィンドウ（09_js_ui 3節）
*/

const worksList = document.getElementById('works-list');
const worksStatus = document.getElementById('works-status');
const filters = document.getElementById('filters');
const dialog = document.getElementById('work-dialog');

let works = [];   // 読み込んだ作品のデータ（モーダルで詳細を表示するときにも使う）

// '2026-09' → '2026年9月'
const formatMonth = (date) => {
    const [year, month] = date.split('-');
    return `${year}年${Number(month)}月`;
};

// タグの一覧（<ul class="tag-list">）の中身を作る
const fillTags = (ul, tags) => {
    ul.textContent = '';
    tags.forEach((tag) => {
        const li = document.createElement('li');
        li.textContent = tag;
        ul.append(li);
    });
};


// ============================================================
// 1. 一覧の表示
// ============================================================
const createWorkCard = (work, index) => {
    const li = document.createElement('li');
    li.className = 'work-card fade-in';
    li.dataset.tags = work.tags.join(' ');

    // カード全体をボタンにして、押すとモーダルが開くようにする（キーボードでも開ける）
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'work-open';
    button.dataset.index = index;

    const title = document.createElement('h2');
    title.textContent = work.title;

    const date = document.createElement('p');
    date.className = 'work-date';
    const time = document.createElement('time');
    time.setAttribute('datetime', work.date);
    time.textContent = formatMonth(work.date);
    date.append(time);

    const description = document.createElement('p');
    description.textContent = work.description;

    const tags = document.createElement('ul');
    tags.className = 'tag-list';
    fillTags(tags, work.tags);

    button.append(title, date, description, tags);
    li.append(button);
    return li;
};

const loadWorks = async () => {
    try {
        const response = await fetch('data/works.json');
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        works = await response.json();
        works.forEach((work, index) => worksList.append(createWorkCard(work, index)));
        worksStatus.textContent = '';
        observeFadeIn(worksList);   // common.js の関数：後から作ったカードもふわっと表示する
    } catch (error) {
        worksStatus.textContent = '作品の読み込みに失敗しました。時間をおいて再読み込みしてください。';
        worksStatus.classList.add('error');
        console.error(error);
    }
};


// ============================================================
// 2. 絞り込み
// ============================================================
const applyFilter = (selected) => {
    document.querySelectorAll('.work-card').forEach((card) => {
        const match = selected === 'all' || card.dataset.tags.split(' ').includes(selected);
        card.classList.toggle('hidden', !match);
    });
};


// ============================================================
// 3. 詳細の表示（モーダルウィンドウ）
// ============================================================
const openDetail = (work) => {
    document.getElementById('dialog-title').textContent = work.title;
    document.getElementById('dialog-date').textContent = formatMonth(work.date);
    document.getElementById('dialog-detail').textContent = work.detail;
    fillTags(document.getElementById('dialog-tags'), work.tags);

    const points = document.getElementById('dialog-points');
    points.textContent = '';
    work.points.forEach((point) => {
        const li = document.createElement('li');
        li.textContent = point;
        points.append(li);
    });

    dialog.showModal();
};


if (worksList) {
    loadWorks();

    filters.addEventListener('click', (event) => {
        const button = event.target.closest('button');
        if (!button) {
            return;
        }
        filters.querySelectorAll('button').forEach((b) => b.classList.remove('active'));
        button.classList.add('active');
        applyFilter(button.dataset.tag);
    });

    // カードは後から作られるので、親の #works-list に1回だけ登録する
    worksList.addEventListener('click', (event) => {
        const button = event.target.closest('.work-open');
        if (button) {
            openDetail(works[Number(button.dataset.index)]);
        }
    });

    document.getElementById('dialog-close').addEventListener('click', () => dialog.close());
    dialog.addEventListener('click', (event) => {
        if (event.target === dialog) {   // 暗い背景をクリックしたとき
            dialog.close();
        }
    });
}
