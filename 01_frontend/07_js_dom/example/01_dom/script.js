// ============================================================
// 1. querySelector と属性の読み書き
// ============================================================
// querySelector() は、CSSのセレクタで要素を1つ取得する（最初に一致したもの）
// querySelectorAll() は、一致したものをすべて取得する
const link = document.querySelector('a.doc-link');           // クラスセレクタ
// document.querySelector('#memo-list')                     // ID も # で指定できる
// document.querySelector('meta[name="csrf-token"]')         // 属性セレクタも使える

// 属性の読み書き
const href = link.getAttribute('href');                     // 属性の値を読む
link.setAttribute('target', '_blank');                      // 属性を追加・変更する
link.setAttribute('rel', 'noopener noreferrer');

// data-* 属性は dataset で読み書きできる（data-lang → dataset.lang）
const lang = link.dataset.lang;

const attrOutput = document.getElementById('attr-output');
attrOutput.textContent = `href=${href} / data-lang=${lang} / target=${link.getAttribute('target')}（JavaScriptで追加）`;


// ============================================================
// 2. 要素を作って追加する
// ============================================================
const memos = [
    { title: '買い物リスト', category: '家事' },
    { title: '企画会議メモ', category: '仕事' },
    { title: '読書メモ：銀河鉄道の夜', category: '趣味' },
];

const list = document.getElementById('memo-list');

memos.forEach((memo) => {
    // 1. createElement() で新しい要素を作る（この時点ではまだ画面に無い）
    const li = document.createElement('li');

    const tag = document.createElement('span');
    tag.className = 'tag';                  // class 属性を設定する
    tag.textContent = memo.category;

    // 2. append() で子要素や文字列を追加する（複数まとめて渡せる）
    li.append(tag, memo.title);

    // 3. 画面上にある要素に追加して、初めて表示される
    list.append(li);
});

// 要素を消すときは remove()
// list.querySelector('li').remove();


// ============================================================
// 3. textContent と innerHTML の違い
// ============================================================
// ユーザーが入力した文字列だと思ってください
const userInput = `<img src=x onerror="alert('乗っ取り')">`;

// textContent：文字列を「ただの文字」として表示する（安全）
document.getElementById('safe-output').textContent = userInput;

// innerHTML：文字列を「HTMLとして解釈」して表示する
// ユーザーの入力を innerHTML に入れると、仕込まれたタグやスクリプトが実行されてしまう（XSS：クロスサイトスクリプティング）
// 確認したいときだけ、次の行のコメントを外す（アラートが出る）
// document.getElementById('danger-output').innerHTML = userInput;
document.getElementById('danger-output').textContent = '（コメントを外すと、ここにHTMLとして挿入されてアラートが出る）';

// ルール：ユーザーの入力や、サーバーから受け取ったデータを表示するときは textContent を使う
