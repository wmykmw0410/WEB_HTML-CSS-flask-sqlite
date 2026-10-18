/*
storage.js：メモのデータを読み込む・保存する（データ担当）

画面の操作は list.js・detail.js・form.js に任せ、このファイルは
「データをどこに・どんな形で保存するか」だけを担当する。
保存先を変えたくなったら、このファイルだけを書き換えればよい
（バックエンド編では、保存先をブラウザからサーバーに移すことになる）。

保存するデータの形（メモ1件）：02_backend/100_memo_api のデータベースの memos テーブルと同じ名前
    {
        "id": 1,                     一意の番号
        "title": "買い物リスト",
        "category": "家事",
        "body": "牛乳、卵…",
        "due_date": "2026-10-07",    期限（無ければ null）
        "is_pinned": true            ピン留めしているか
    }
*/

const STORAGE_KEY = 'memo-app.memos';


// ============================================================
// ステップ1：localStorage からメモの配列を読み出す。まだ保存されていなければ null
// ============================================================
const loadMemos = () => {
    const json = localStorage.getItem(STORAGE_KEY);
    return json ? JSON.parse(json) : null;
};


// ============================================================
// ステップ1：メモの配列を localStorage に保存する
// ============================================================
const saveMemos = (memos) => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(memos));
};


// ============================================================
// ステップ1：メモの配列を用意する（async 関数）
// - localStorage に保存されていれば、それを返す
// - 初めて開いたとき（保存されていないとき）は、data/memos.json を初期データとして読み込み、
//   localStorage に保存してから返す
// ============================================================
const initMemos = async () => {
    const saved = loadMemos();
    if (saved) {
        return saved;
    }

    const response = await fetch('data/memos.json');
    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
    }
    const memos = await response.json();
    saveMemos(memos);
    return memos;
};


// ============================================================
// 以下は完成済み
// ============================================================

// 保存したデータを消す（次に開いたときは初期データから始まる）
const resetMemos = () => {
    localStorage.removeItem(STORAGE_KEY);
};

// 新しいメモに付けるID：今あるIDの最大値 + 1（1件も無ければ 1）
const nextId = (memos) => {
    let max = 0;
    memos.forEach((memo) => {
        if (memo.id > max) {
            max = memo.id;
        }
    });
    return max + 1;
};

// URL の ?id=3 を数値で返す（無ければ null）。detail.html・edit.html で使う
const getIdFromUrl = () => {
    const params = new URLSearchParams(location.search);   // location.search は '?id=3'
    const id = params.get('id');                            // '3'（無ければ null）
    return id === null ? null : Number(id);                 // 文字列なので数値にする
};

// 「あると便利」な設定（選んだカテゴリなど）の保存と読み出し。
// localStorage が使えない環境でもページが止まらないよう、try/catch で囲む（01_frontend/10_js_data 4節）
const saveSetting = (key, value) => {
    try {
        localStorage.setItem(key, value);
    } catch (error) {
        // 保存できなくても、ページはそのまま動く
    }
};

const loadSetting = (key) => {
    try {
        return localStorage.getItem(key);
    } catch (error) {
        return null;
    }
};
