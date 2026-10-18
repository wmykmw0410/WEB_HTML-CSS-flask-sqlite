// 解答4：作品一覧を、タグとキーワードの両方で絞り込む

const buttons = document.querySelectorAll('.filters button');
const works = document.querySelectorAll('.work');
const keywordInput = document.getElementById('keyword');
const count = document.getElementById('count');
const empty = document.getElementById('empty');

// 今選ばれているタグ。ボタンが押されたら書き換える
let selectedTag = 'all';


// TODO 1：今の条件で、作品の表示・非表示を切り替える
// タグのボタンと検索欄のどちらが操作されても、この関数1つで「両方の条件」を見て決め直す
const applyFilter = () => {
    const keyword = keywordInput.value.trim();
    let shown = 0;

    works.forEach((work) => {
        const tags = work.dataset.tags.split(' ');              // 'HTML CSS' → ['HTML', 'CSS']
        const title = work.querySelector('h3').textContent;

        const tagMatch = selectedTag === 'all' || tags.includes(selectedTag);
        const keywordMatch = title.includes(keyword);           // 空欄なら includes('') は常に true

        const match = tagMatch && keywordMatch;
        work.hidden = !match;
        if (match) {
            shown++;
        }
    });

    count.textContent = `${shown}件表示中`;
    empty.hidden = shown > 0;
};


// TODO 2：タグのボタン
buttons.forEach((button) => {
    button.addEventListener('click', () => {
        buttons.forEach((b) => b.setAttribute('aria-pressed', 'false'));
        button.setAttribute('aria-pressed', 'true');

        selectedTag = button.dataset.tag;
        applyFilter();
    });
});


// TODO 3：検索欄
keywordInput.addEventListener('input', applyFilter);
// () => applyFilter() と書いてもよい。applyFilter() と () を付けると、その場で1回呼ばれるだけになる
