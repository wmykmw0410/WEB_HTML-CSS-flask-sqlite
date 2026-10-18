const buttons = document.querySelectorAll('.filters button');
const cards = document.querySelectorAll('.card');

// querySelectorAll() は条件に一致する要素の一覧（NodeList）を返す
buttons.forEach((button) => {
    button.addEventListener('click', () => {
        // 1. クリックされたボタンにだけ active クラスを付け直す
        buttons.forEach((b) => b.classList.remove('active'));
        button.classList.add('active');

        const selected = button.dataset.category;   // data-category="..." の値を取得

        // 2. サーバーに問い合わせず、すでに画面上にあるカードの表示/非表示だけを切り替える
        cards.forEach((card) => {
            const match = selected === 'all' || card.dataset.category === selected;
            card.classList.toggle('hidden', !match);
        });
    });
});
