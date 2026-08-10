/*
018_ownership_crudで作ったメモ帳アプリに、JavaScriptで3つの機能を追加したもの。

このファイルは全ページで読み込まれるため、対象の要素がそのページに
無いこともある。`if (要素)` で存在チェックしてから使う。
*/

// ============================================================
// 問題1：文字数カウンター（メモ追加・編集ページ）
// ============================================================
const bodyTextarea = document.getElementById('body');
if (bodyTextarea) {
    const counter = document.getElementById('body-count');

    const updateCount = () => {
        const length = bodyTextarea.value.length;
        counter.textContent = length;
        counter.classList.toggle('over', length > 500);
    };

    bodyTextarea.addEventListener('input', updateCount);
    updateCount();   // 編集ページを開いた直後（既存の本文が入っている状態）の表示も合わせておく
}


// ============================================================
// 問題2：カテゴリの絞り込み（メモ一覧ページ）
// ============================================================
const filterButtons = document.querySelectorAll('.filters button');
if (filterButtons.length > 0) {
    const cards = document.querySelectorAll('.card');

    filterButtons.forEach((button) => {
        button.addEventListener('click', () => {
            filterButtons.forEach((b) => b.classList.remove('active'));
            button.classList.add('active');

            const selected = button.dataset.category;

            cards.forEach((card) => {
                const match = selected === 'all' || card.dataset.category === selected;
                card.classList.toggle('hidden', !match);
            });
        });
    });
}


// ============================================================
// 問題3：ピン留めをfetch()でトグルする（メモ一覧ページ）
// ============================================================
const pinButtons = document.querySelectorAll('.pin-button');
if (pinButtons.length > 0) {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

    pinButtons.forEach((button) => {
        button.addEventListener('click', async () => {
            const memoId = button.dataset.id;

            const response = await fetch(`/memos/${memoId}/toggle-pin`, {
                method: 'POST',
                headers: { 'X-CSRFToken': csrfToken },
            });
            const data = await response.json();

            button.textContent = data.is_pinned ? '★' : '☆';
        });
    });
}
