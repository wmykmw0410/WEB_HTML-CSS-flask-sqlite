/*
form.js：メモの追加ページ（new.html）と編集ページ（edit.html）の処理

2つのページは同じフォームを使う。URL に ?id=3 のような指定があれば「編集」、無ければ「追加」として動く。
*/

const form = document.getElementById('memo-form');
const formStatus = document.getElementById('form-status');
const titleInput = document.getElementById('title');
const categoryInput = document.getElementById('category');
const bodyInput = document.getElementById('body');
const dueInput = document.getElementById('due_date');
const counter = document.getElementById('body-count');
const draftStatus = document.getElementById('draft-status');   // 追加ページにだけある

const editId = getIdFromUrl();   // edit.html?id=3 なら 3、new.html なら null（storage.js）

let memos = [];
let editingMemo = null;   // 編集中のメモ（追加ページでは null のまま）


// ============================================================
// 文字数カウンター（完成済み：01_frontend/06_js_events 練習問題1）
// ============================================================
const updateCount = () => {
    const length = bodyInput.value.length;
    counter.textContent = length;
    counter.parentElement.classList.toggle('over', length > 500);
};
bodyInput.addEventListener('input', updateCount);


// ============================================================
// 入力チェック（完成済み：01_frontend/06_js_events 練習問題2）
// ============================================================
const showError = (input, message) => {
    document.getElementById(`${input.id}-error`).textContent = message;
    input.classList.toggle('invalid', message !== '');
};

const validate = () => {
    const title = titleInput.value.trim();
    const body = bodyInput.value.trim();

    let titleMessage = '';
    if (!title) {
        titleMessage = 'タイトルを入力してください';
    } else if (title.length > 100) {
        titleMessage = 'タイトルは100文字以内で入力してください';
    }

    let bodyMessage = '';
    if (!body) {
        bodyMessage = '本文を入力してください';
    } else if (body.length > 500) {
        bodyMessage = '本文は500文字以内で入力してください';
    }

    showError(titleInput, titleMessage);
    showError(bodyInput, bodyMessage);
    return !titleMessage && !bodyMessage;   // エラーが1つも無ければ true
};


// ============================================================
// 下書きの自動保存（完成済み：01_frontend/10_js_data 4節のサンプル）。追加ページだけで動く
// ============================================================
const DRAFT_KEY = form.dataset.draftKey;   // new.html の <form data-draft-key="memo-draft">。edit.html では undefined
const draftInputs = [titleInput, categoryInput, bodyInput, dueInput];

const saveDraft = () => {
    const draft = { savedAt: new Date().toLocaleTimeString() };
    draftInputs.forEach((input) => {
        draft[input.id] = input.value;
    });
    saveSetting(DRAFT_KEY, JSON.stringify(draft));   // storage.js
    draftStatus.textContent = `下書きを保存しました（${draft.savedAt}）`;
};

const restoreDraft = () => {
    const json = loadSetting(DRAFT_KEY);
    if (!json) {
        return;
    }
    const draft = JSON.parse(json);
    draftInputs.forEach((input) => {
        if (draft[input.id] !== undefined) {
            input.value = draft[input.id];
        }
    });
    draftStatus.textContent = `${draft.savedAt} に保存した下書きを復元しました`;
};

if (DRAFT_KEY) {
    restoreDraft();
    form.addEventListener('input', saveDraft);
}


// ============================================================
// ステップ5：編集ページでは、フォームに今の内容を入れておく
// ============================================================
const fillForm = (memo) => {
    titleInput.value = memo.title;
    categoryInput.value = memo.category;   // select も .value で選択肢を選べる
    bodyInput.value = memo.body;
    dueInput.value = memo.due_date ?? '';  // null なら空欄
};


// ============================================================
// ステップ4・5：保存
// ============================================================
form.addEventListener('submit', (event) => {
    event.preventDefault();   // サーバーに送信するのではなく、JavaScriptで保存する
    if (!validate()) {
        document.querySelector('.invalid').focus();   // 最初のエラーの欄に移動する
        return;
    }

    const values = {
        title: titleInput.value.trim(),
        category: categoryInput.value,
        body: bodyInput.value.trim(),
        due_date: dueInput.value || null,   // 空欄（''）なら null にする
    };

    let savedId;
    if (editingMemo) {
        // 編集：見つけたメモのプロパティを書き換える（配列の中の同じオブジェクトが変わる）
        Object.assign(editingMemo, values);
        savedId = editingMemo.id;
    } else {
        // 追加：新しいメモを配列に追加する
        savedId = nextId(memos);
        memos.push({ id: savedId, is_pinned: false, ...values });
        if (DRAFT_KEY) {
            saveSetting(DRAFT_KEY, '');   // 保存したので下書きは空にする
        }
    }

    saveMemos(memos);
    location.href = `detail.html?id=${savedId}`;   // 保存したメモの詳細ページに移動する（100_memo_api と同じ）
});
// 補足：
//   Object.assign(対象, 値) は、値のオブジェクトのプロパティをまとめて対象に書き込む
//   { id: 1, ...values } の ... はスプレッド構文。values のプロパティをここに展開する


// ============================================================
// 入力途中のキャンセル確認（完成済み）
// ============================================================
const hasChanges = () => {
    if (editingMemo) {
        return titleInput.value !== editingMemo.title
            || categoryInput.value !== editingMemo.category
            || bodyInput.value !== editingMemo.body
            || dueInput.value !== (editingMemo.due_date ?? '');
    }
    return Boolean(titleInput.value.trim() || bodyInput.value.trim());
};

document.getElementById('cancel-link').addEventListener('click', (event) => {
    if (!hasChanges()) {
        return;   // 何も変えていなければ、そのままリンク先へ
    }
    event.preventDefault();   // いったん移動を止めて、確認する
    openConfirm('入力内容が破棄されます。よろしいですか？', () => {   // common.js
        if (DRAFT_KEY) {
            saveSetting(DRAFT_KEY, '');   // 下書きも消す
        }
        location.href = event.target.href;
    });
});


// ============================================================
// ページを開いたときの処理
// ============================================================
const start = async () => {
    try {
        memos = await initMemos();   // 追加ページで開いた場合も、ID を決めるのに全メモが必要
    } catch (error) {
        console.error(error);
        formStatus.textContent = 'メモを読み込めませんでした。python -m http.server で起動して開いているか確認してください。';
        form.hidden = true;
        return;
    }

    if (editId !== null) {
        // ステップ5：URL の ?id= のメモを探して、フォームに入れる
        editingMemo = memos.find((memo) => memo.id === editId);
        if (!editingMemo) {
            formStatus.textContent = '指定されたメモが見つかりません。';
            formStatus.classList.add('error');
            form.hidden = true;
            return;
        }
        fillForm(editingMemo);
    }

    updateCount();   // 編集中のメモや、復元した下書きの文字数を表示する
};

start();
