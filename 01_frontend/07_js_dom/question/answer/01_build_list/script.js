// 解答1：JavaScriptで要素を作って書き換える

const memos = [
    { title: '買い物リスト', category: '家事' },
    { title: '企画会議メモ', category: '仕事' },
    { title: '読書メモ：銀河鉄道の夜', category: '趣味' },
];

// ユーザーが入力した文字だと思ってください（タグを含んでいる）
const userInput = `<img src=x onerror="alert('乗っ取り')">`;


// TODO 1：createElement で作り、append で画面上の要素に追加して、初めて表示される
const list = document.getElementById('memo-list');
memos.forEach((memo) => {
    const li = document.createElement('li');

    const tag = document.createElement('span');
    tag.className = 'tag';
    tag.textContent = memo.category;

    li.append(tag, memo.title);   // append は複数まとめて渡せる（文字列も渡せる）
    list.append(li);
});


// TODO 2：querySelector は CSS のセレクタで要素を1つ取得する
const link = document.querySelector('a.doc-link');
link.setAttribute('target', '_blank');
link.setAttribute('rel', 'noopener noreferrer');   // target="_blank" とセットで付ける


// TODO 3：data-lang="ja" は dataset.lang で読める
document.getElementById('lang-output').textContent = `言語：${link.dataset.lang}`;


// TODO 4：ユーザーの入力は textContent で入れる（innerHTML だとタグとして解釈され、XSS の原因になる）
document.getElementById('user-output').textContent = userInput;
