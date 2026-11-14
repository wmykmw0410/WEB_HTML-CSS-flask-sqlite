// localStorage：ブラウザの中に「キーと値」の組を保存できる仕組み。
// ページを閉じても、ブラウザを再起動しても消えない（ユーザーが消すまで残る）。
//   localStorage.setItem('キー', '値');   保存する
//   localStorage.getItem('キー');         読み出す（無ければ null）
//   localStorage.removeItem('キー');      1件消す
// 保存できるのは「文字列」だけ。数値や配列・オブジェクトは変換して保存する。


// ============================================================
// 1. 訪問回数（数値を保存する）
// ============================================================
// getItem() は文字列か null を返すので、Number() で数値に変換する（null → 0）
const visits = Number(localStorage.getItem('visitCount')) + 1;
localStorage.setItem('visitCount', visits);   // 数値は自動で文字列 '3' などになる
document.getElementById('visit-count').textContent = visits;


// ============================================================
// 2. 下書きの自動保存（文字列を保存する）
// ============================================================
const draft = document.getElementById('draft');
const savedMessage = document.getElementById('saved-message');

// ページを開いたときに、保存されている下書きを復元する（無ければ空文字）
draft.value = localStorage.getItem('draft') ?? '';

draft.addEventListener('input', () => {
    localStorage.setItem('draft', draft.value);
    savedMessage.textContent = `保存しました（${draft.value.length}文字）`;
});
// 補足：?? は「左側が null または undefined のときだけ、右側の値を使う」という演算子


// ============================================================
// 3. 設定の保存（オブジェクトを JSON にして保存する）
// ============================================================
const SETTINGS_KEY = 'settings';
const largeCheckbox = document.getElementById('setting-large');

// 読み出し：JSON文字列 → オブジェクト。保存されていなければ初期値を使う
const loadSettings = () => {
    const json = localStorage.getItem(SETTINGS_KEY);
    return json ? JSON.parse(json) : { large: false };
};

// 保存：オブジェクト → JSON文字列
const saveSettings = (settings) => {
    localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings));
};

const applySettings = (settings) => {
    largeCheckbox.checked = settings.large;
    document.body.style.fontSize = settings.large ? '1.25rem' : '';
};

applySettings(loadSettings());

largeCheckbox.addEventListener('change', () => {
    const settings = { large: largeCheckbox.checked };
    saveSettings(settings);
    applySettings(settings);
});

// オブジェクトをそのまま setItem() すると、'[object Object]' という意味のない文字列になってしまう
// localStorage.setItem('bad', { large: true });  →  保存されるのは '[object Object]'


// ============================================================
// 4. すべて消す
// ============================================================
document.getElementById('clear').addEventListener('click', () => {
    if (!confirm('保存したデータをすべて消しますか？')) {
        return;
    }
    localStorage.removeItem('visitCount');
    localStorage.removeItem('draft');
    localStorage.removeItem(SETTINGS_KEY);
    location.reload();   // ページを読み込み直す
});
