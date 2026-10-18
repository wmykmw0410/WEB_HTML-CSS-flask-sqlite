// 解答3：ダークモードの設定を localStorage に保存する

const STORAGE_KEY = 'theme';
const toggle = document.getElementById('theme-toggle');
const updatedAt = document.getElementById('updated-at');


// TODO 1：読み出し
const loadTheme = () => {
    const json = localStorage.getItem(STORAGE_KEY);
    return json ? JSON.parse(json) : { dark: false, updatedAt: null };
};


// TODO 2：保存
const saveTheme = (theme) => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(theme));
};


// TODO 3：反映
const applyTheme = (theme) => {
    document.body.classList.toggle('dark', theme.dark);
    toggle.textContent = theme.dark ? 'ライトモードにする' : 'ダークモードにする';
    updatedAt.textContent = theme.updatedAt ?? 'まだありません';
};


// TODO 4：開いたときに反映し、押されたら「反転 → 保存 → 反映」
let theme = loadTheme();
applyTheme(theme);

toggle.addEventListener('click', () => {
    theme = { dark: !theme.dark, updatedAt: new Date().toLocaleString() };
    saveTheme(theme);
    applyTheme(theme);
});
