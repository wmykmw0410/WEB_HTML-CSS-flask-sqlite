/*
山田太郎のポートフォリオサイト 共通スクリプト（全ページで読み込む）
ページによって対象の要素が無いので、if (要素) で存在を確認してから使う。
*/

// ============================================================
// ハンバーガーメニュー（全ページ）
// ============================================================
const navToggle = document.getElementById('nav-toggle');
if (navToggle) {
    const navLinks = document.getElementById('nav-links');

    navToggle.addEventListener('click', () => {
        navLinks.classList.toggle('open');
    });
}

// ============================================================
// 10_js_data で変更：制作実績を data/works.json から読み込んで表示する（works.html）
// ============================================================
const worksList = document.getElementById('works-list');
const filters = document.getElementById('filters');

// 作品1件分のカードを作る（テキストは textContent で入れる）
const createWorkCard = (work) => {
    const li = document.createElement('li');
    li.className = 'work-card';
    li.dataset.tags = work.tags.join(' ');

    const title = document.createElement('h2');
    title.textContent = work.title;

    const date = document.createElement('p');
    date.className = 'work-date';
    const time = document.createElement('time');
    const [year, month] = work.date.split('-');
    time.setAttribute('datetime', work.date);
    time.textContent = `${year}年${Number(month)}月`;
    date.append(time);

    const description = document.createElement('p');
    description.textContent = work.description;

    const tagList = document.createElement('ul');
    tagList.className = 'tag-list';
    work.tags.forEach((tag) => {
        const item = document.createElement('li');
        item.textContent = tag;
        tagList.append(item);
    });

    li.append(title, date, description, tagList);
    return li;
};

// 選ばれたタグに合うカードだけを表示する
const applyFilter = (selected) => {
    document.querySelectorAll('.work-card').forEach((card) => {
        const tags = card.dataset.tags.split(' ');
        card.classList.toggle('hidden', !(selected === 'all' || tags.includes(selected)));
    });
};

const loadWorks = async () => {
    const status = document.getElementById('works-status');
    try {
        const response = await fetch('data/works.json');
        if (!response.ok) {
            throw new Error(`読み込みに失敗しました（${response.status}）`);
        }
        const works = await response.json();

        works.forEach((work) => worksList.append(createWorkCard(work)));
        status.textContent = '';
    } catch (error) {
        status.textContent = '作品の読み込みに失敗しました。時間をおいて再読み込みしてください。';
        status.classList.add('error');
        console.error(error);
    }
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
}

// ============================================================
// お問い合わせフォームの入力チェック（contact.html）
// ============================================================
const contactForm = document.getElementById('contact-form');
if (contactForm) {
    const result = document.getElementById('contact-result');

    // エラーメッセージの表示・非表示を切り替える
    const showError = (input, message) => {
        document.getElementById(`${input.id}-error`).textContent = message;
        input.classList.toggle('invalid', message !== '');
    };

    contactForm.addEventListener('submit', (event) => {
        // このサイトは静的なページなので、送信先のサーバーが無い。送信は止めてメッセージだけ表示する
        event.preventDefault();

        const name = document.getElementById('name');
        const email = document.getElementById('email');
        const message = document.getElementById('message');

        showError(name, name.value.trim() ? '' : 'お名前を入力してください');
        showError(email, email.value.includes('@') ? '' : 'メールアドレスの形式で入力してください');
        showError(message, message.value.trim().length >= 10 ? '' : 'メッセージは10文字以上で入力してください');

        if (contactForm.querySelector('.invalid')) {
            result.textContent = '';
            return;
        }

        result.textContent = `${name.value.trim()}さん、お問い合わせありがとうございました。（この作例では実際には送信されません）`;
        contactForm.reset();
    });
}
