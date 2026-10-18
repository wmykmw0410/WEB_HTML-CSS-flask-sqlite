/*
メモ帳アプリの script.js。フロントエンド編で学んだ機能を、Flask で作ったページに追加している。
（02_backend/02_memo_app_frontend の common.js・list.js・form.js と同じ書き方）

このファイルは全ページで読み込まれるため、対象の要素がそのページに無いこともある。
各機能は「要素があるときだけ」動くように、関数の最初で存在をチェックしている。

見出しの記号は、README の「フロントエンド編から取り入れた項目」の表に対応している。
*/


// ============================================================
// 共通：自動で消える通知（J2：01_frontend/09_js_ui 2節）
// ============================================================
const toast = document.getElementById('toast');
let toastTimer = null;

const showToast = (message, isError = false) => {
    toast.textContent = message;
    toast.classList.toggle('error', isError);
    // すでに開いているときに showPopover() するとエラーになるので、閉じているときだけ開く
    if (!toast.matches(':popover-open')) {
        toast.showPopover();
    }
    // 連続で呼ばれたら、前のタイマーを取り消して、そこから数え直す
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
        toast.hidePopover();
    }, 3000);
};


// ============================================================
// 全ページ：flash() のメッセージを通知で表示する（J2）
// サーバーが base.html に出力した #flash の一覧を読み、通知に出してから一覧を隠す。
// JavaScript が動かないときは、一覧がそのまま表示される
// ============================================================
const setupFlash = () => {
    const flashList = document.getElementById('flash');
    if (!flashList) {
        return;
    }
    const messages = [];
    flashList.querySelectorAll('li').forEach((li) => messages.push(li.textContent));
    showToast(messages.join(' '));
    flashList.hidden = true;
};


// ============================================================
// 全ページ：ハンバーガーメニュー（01_frontend/08_js_render の制作課題）
// ============================================================
const setupNav = () => {
    const navToggle = document.getElementById('nav-toggle');
    const navLinks = document.getElementById('nav-links');

    navToggle.addEventListener('click', () => {
        const isOpen = navLinks.classList.toggle('open');
        navToggle.setAttribute('aria-expanded', isOpen);
        navToggle.setAttribute('aria-label', isOpen ? 'メニューを閉じる' : 'メニューを開く');
    });
};


// ============================================================
// 全ページ：配色の切り替え（J5：01_frontend/10_js_data 4節の「応用」）
// 読み込み直後の反映は base.html の <head> で行っている。ここではボタンでの切り替えだけを書く
// ============================================================
const setupTheme = () => {
    const button = document.getElementById('theme-toggle');
    const root = document.documentElement;

    // 今の配色：ボタンで選んだもの（data-theme）が無ければ、OS の設定に従う
    const currentTheme = () => {
        if (root.dataset.theme) {
            return root.dataset.theme;
        }
        return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    };

    const updateLabel = () => {
        const next = currentTheme() === 'dark' ? 'ライト' : 'ダーク';
        button.setAttribute('aria-label', `${next}モードに切り替える`);
        button.title = `${next}モードに切り替える`;
    };

    button.addEventListener('click', () => {
        const next = currentTheme() === 'dark' ? 'light' : 'dark';
        root.dataset.theme = next;
        try {
            localStorage.setItem('theme', next);
        } catch (error) {
            // 保存できなくても、このページの表示は切り替わっているので何もしない
        }
        updateLabel();
    });

    updateLabel();
};


// ============================================================
// 全ページ：スクロール（J8：01_frontend/09_js_ui 5節）
//   - 少しスクロールしたらヘッダーに影
//   - 300px 以上スクロールしたら「トップへ戻る」ボタン
//   - カードは、画面に入ったらふわっと表示（IntersectionObserver）
// ============================================================
const setupScroll = () => {
    const header = document.querySelector('.site-header');
    const toTop = document.getElementById('to-top');

    const onScroll = () => {
        const y = window.scrollY;
        header.classList.toggle('scrolled', y > 10);
        toTop.hidden = y < 300;
    };
    window.addEventListener('scroll', onScroll);
    onScroll();

    toTop.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
};

// observer は1つだけ作って、すべてのカードで使い回す
const fadeInObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            fadeInObserver.unobserve(entry.target);   // 一度表示したら、もう監視しない
        }
    });
}, { threshold: 0.1 });

// fade-in クラス（最初は透明）は、HTML ではなくここで付ける。
// JavaScript が動かない環境でも、カードが透明のまま残らないようにするため
const observeFadeIn = (elements) => {
    elements.forEach((el) => {
        el.classList.add('fade-in');
        fadeInObserver.observe(el);
    });
};


// ============================================================
// 全ページ：削除の確認ダイアログ（J3：01_frontend/09_js_ui 3節「確認してから送信する」）
// data-confirm を持つフォームは、送信の前に <dialog> で確認する
// ============================================================
const setupConfirmForms = () => {
    const dialog = document.getElementById('confirm-dialog');
    const message = document.getElementById('confirm-message');
    let pendingForm = null;   // 確認中のフォーム（OK が押されたら送信する）

    document.querySelectorAll('form[data-confirm]').forEach((form) => {
        form.addEventListener('submit', (event) => {
            event.preventDefault();   // いったん送信を止めて、ダイアログを開く
            pendingForm = form;
            message.textContent = form.dataset.confirm;
            dialog.showModal();
        });
    });

    document.getElementById('confirm-ok').addEventListener('click', () => {
        dialog.close();
        pendingForm.submit();   // form.submit() は submit イベントを起こさないので、もう一度確認されることはない
    });

    document.getElementById('confirm-cancel').addEventListener('click', () => {
        dialog.close();
    });

    // 暗い背景（dialog 自身）をクリックしたら閉じる。Esc キーではブラウザが閉じてくれる
    dialog.addEventListener('click', (event) => {
        if (event.target === dialog) {
            dialog.close();
        }
    });
};


// ============================================================
// メモ一覧：カテゴリ＋キーワードの絞り込み（H3・J4・J5）
//   01_frontend/08_js_render 3節・練習問題3、10_js_data の制作課題（選んだ絞り込みを覚える）
// ============================================================
const setupFilters = () => {
    const buttons = document.querySelectorAll('.filters button');
    const keywordInput = document.getElementById('keyword');
    if (buttons.length === 0 || !keywordInput) {
        return;
    }
    const cards = document.querySelectorAll('#card-grid .card');
    const count = document.getElementById('list-count');
    const empty = document.getElementById('empty');
    const STORAGE_KEY = 'memo-filter';

    let selectedCategory = 'all';

    const applyFilter = () => {
        const keyword = keywordInput.value.trim();
        let shown = 0;

        cards.forEach((card) => {
            const text = card.querySelector('.card-link').textContent;
            const categoryMatch = selectedCategory === 'all' || card.dataset.category === selectedCategory;
            const keywordMatch = text.includes(keyword);
            const match = categoryMatch && keywordMatch;
            card.hidden = !match;
            if (match) {
                shown++;
            }
        });

        count.textContent = `${cards.length}件中 ${shown}件を表示`;
        empty.hidden = shown > 0;
    };

    const selectCategory = (category) => {
        selectedCategory = category;
        buttons.forEach((b) => {
            b.setAttribute('aria-pressed', b.dataset.category === category);
        });
        applyFilter();
    };

    buttons.forEach((button) => {
        button.addEventListener('click', () => {
            selectCategory(button.dataset.category);
            try {
                localStorage.setItem(STORAGE_KEY, button.dataset.category);
            } catch (error) {
                // 保存できなくても絞り込みは動く
            }
        });
    });

    keywordInput.addEventListener('input', applyFilter);

    // 前回選んだカテゴリを復元する（そのカテゴリのボタンがあるときだけ）
    let saved = null;
    try {
        saved = localStorage.getItem(STORAGE_KEY);
    } catch (error) {
        saved = null;
    }
    const savedButton = saved ? document.querySelector(`.filters button[data-category="${saved}"]`) : null;
    selectCategory(savedButton ? saved : 'all');
};


// ============================================================
// メモの追加・編集：文字数カウンター（01_frontend/06_js_events 練習問題1）
// ============================================================
const setupCharCount = () => {
    const bodyTextarea = document.getElementById('body');
    const counter = document.getElementById('body-count');
    if (!bodyTextarea || !counter) {
        return;
    }
    const counterText = counter.parentElement;

    const updateCount = () => {
        const length = bodyTextarea.value.length;
        counter.textContent = length;
        counterText.classList.toggle('over', length > 500);
    };

    bodyTextarea.addEventListener('input', updateCount);
    updateCount();   // 編集ページや下書きの復元で、最初から本文が入っているときの表示も合わせておく
};


// ============================================================
// メモの追加・編集：送信前の入力チェック（J7：01_frontend/06_js_events 練習問題2）
// サーバー側（WTForms）のチェックは残したまま、送信する前に気づけるようにする
// ============================================================
const setupValidation = () => {
    const form = document.querySelector('form[data-validate]');
    if (!form) {
        return;
    }
    const titleInput = document.getElementById('title');
    const bodyInput = document.getElementById('body');
    const titleError = form.querySelector('[data-error-for="title"]');
    const bodyError = form.querySelector('[data-error-for="body"]');

    // エラー表示を切り替える（message が空文字なら「エラーなし」）
    const showError = (input, errorEl, message) => {
        errorEl.textContent = message;
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

        showError(titleInput, titleError, titleMessage);
        showError(bodyInput, bodyError, bodyMessage);
        return titleMessage === '' && bodyMessage === '';
    };

    form.addEventListener('submit', (event) => {
        if (!validate()) {
            event.preventDefault();
            form.querySelector('.invalid').focus();   // 最初のエラーの欄に移動する
            return;
        }
        // 送信できる内容になったら、下書きは消しておく（J6）
        if (form.dataset.draftKey) {
            localStorage.removeItem(form.dataset.draftKey);
        }
    });
};


// ============================================================
// メモの追加：下書きの自動保存（J6：01_frontend/10_js_data 4節のサンプル）
// setupCharCount() より先に呼ぶ（復元した本文の文字数が、カウンターに反映されるように）
// ============================================================
const setupDraft = () => {
    const form = document.querySelector('form[data-draft-key]');
    if (!form) {
        return;
    }
    const key = form.dataset.draftKey;
    const status = document.getElementById('draft-status');
    const ids = ['title', 'category', 'body', 'due_date'];   // WTForms は name と同じ id を付ける

    const save = () => {
        const draft = { savedAt: new Date().toLocaleTimeString() };
        ids.forEach((id) => {
            draft[id] = document.getElementById(id).value;
        });
        localStorage.setItem(key, JSON.stringify(draft));
        status.textContent = `下書きを保存しました（${draft.savedAt}）`;
    };

    // 保存されている下書きがあり、入力欄が空なら復元する
    // （サーバー側のチェックで戻ってきたときは、送った内容が入っているので上書きしない）
    const json = localStorage.getItem(key);
    const isEmpty = !document.getElementById('title').value && !document.getElementById('body').value;
    if (json && isEmpty) {
        const draft = JSON.parse(json);
        ids.forEach((id) => {
            if (draft[id] !== undefined) {
                document.getElementById(id).value = draft[id];
            }
        });
        status.textContent = `${draft.savedAt} に保存した下書きを復元しました`;
    }

    form.addEventListener('input', save);
};


// ============================================================
// 実行
// ============================================================
setupFlash();
setupNav();
setupTheme();
setupScroll();
setupConfirmForms();
setupFilters();
setupDraft();        // setupCharCount() より先に（復元した本文の文字数を数えるため）
setupCharCount();
setupValidation();
observeFadeIn(document.querySelectorAll('#card-grid .card'));
