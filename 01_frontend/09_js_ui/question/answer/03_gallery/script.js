// 解答3：ポップアップで作品を順番に見られるギャラリー

const thumbs = Array.from(document.querySelectorAll('.thumb'));
const dialog = document.getElementById('viewer-dialog');
const viewer = document.getElementById('viewer');
const counter = document.getElementById('counter');

let current = 0;


// TODO 1：n 番目の作品を表示する
const show = (n) => {
    current = (n + thumbs.length) % thumbs.length;
    const thumb = thumbs[current];
    viewer.style.background = thumb.dataset.color;
    viewer.textContent = thumb.dataset.title;
    counter.textContent = `${current + 1} / ${thumbs.length}`;
};


// TODO 2：作品をクリックしたら開く
document.getElementById('gallery').addEventListener('click', (event) => {
    const thumb = event.target.closest('.thumb');
    if (!thumb) {
        return;
    }
    show(thumbs.indexOf(thumb));
    dialog.showModal();
});


// TODO 3：前・次・閉じる
document.getElementById('prev').addEventListener('click', () => show(current - 1));
document.getElementById('next').addEventListener('click', () => show(current + 1));
document.getElementById('close').addEventListener('click', () => dialog.close());

dialog.addEventListener('click', (event) => {
    if (event.target === dialog) {   // 暗い背景をクリックしたとき
        dialog.close();
    }
});


// TODO 4：開いている間だけ ← → キーで切り替える
document.addEventListener('keydown', (event) => {
    if (!dialog.open) {
        return;
    }
    if (event.key === 'ArrowLeft') {
        show(current - 1);
    } else if (event.key === 'ArrowRight') {
        show(current + 1);
    }
});
