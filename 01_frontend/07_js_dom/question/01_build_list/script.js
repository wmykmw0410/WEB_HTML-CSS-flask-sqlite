const memos = [
    { title: '買い物リスト', category: '家事' },
    { title: '企画会議メモ', category: '仕事' },
    { title: '読書メモ：銀河鉄道の夜', category: '趣味' },
];

// ユーザーが入力した文字だと思ってください（タグを含んでいる）
const userInput = `<img src=x onerror="alert('乗っ取り')">`;


// TODO 1：memos を、#memo-list の中に li として追加する
//         各 li は <span class="tag">カテゴリ</span> のあとにタイトルが続く形にする


// TODO 2：a.doc-link を querySelector で取得し、新しいタブで開くようにする
//         （target="_blank" と rel="noopener noreferrer" を setAttribute で付ける）


// TODO 3：a.doc-link の data-lang の値を dataset で読み、#lang-output に「言語：ja」と表示する


// TODO 4：userInput を #user-output に表示する（安全な方法で。HTMLとして解釈されないようにする）
