// スライドショーの考え方
//   - 「今何枚目か」を current という変数（状態）で持つ
//   - show(n) で current を n にし、n 枚目のスライドだけに active クラスを付ける
//   - 前へ・次へ・ドット・自動再生は、すべて show() を呼ぶだけにする

const slideshow = document.getElementById('slideshow');
const slides = slideshow.querySelectorAll('.slide');
const dotsArea = document.getElementById('dots');
const statusEl = document.getElementById('status');

let current = 0;        // 今表示しているスライドの番号（0 始まり）
let timerId = null;     // 自動再生のタイマーの番号（止めるときに使う）


// ============================================================
// ドットを作る（スライドの数だけボタンを作る）
// ============================================================
const dots = [];
slides.forEach((slide, index) => {   // forEach の2つ目の引数は、何番目か（0 始まり）
    const dot = document.createElement('button');
    dot.type = 'button';
    dot.setAttribute('aria-label', `${index + 1}枚目を表示`);
    dot.addEventListener('click', () => show(index));
    dotsArea.append(dot);
    dots.push(dot);
});


// ============================================================
// n 枚目を表示する
// ============================================================
const show = (n) => {
    // 範囲外の番号を、最後 → 最初・最初 → 最後に回り込ませる
    current = (n + slides.length) % slides.length;

    slides.forEach((slide, index) => {
        slide.classList.toggle('active', index === current);
    });
    dots.forEach((dot, index) => {
        dot.setAttribute('aria-current', index === current);
    });
};

slideshow.querySelector('.prev').addEventListener('click', () => show(current - 1));
slideshow.querySelector('.next').addEventListener('click', () => show(current + 1));


// ============================================================
// 自動再生：setInterval(関数, ミリ秒) で一定時間ごとに関数を呼ぶ
// ============================================================
const start = () => {
    if (timerId !== null) {
        return;   // すでに動いていれば何もしない（タイマーを二重に作らない）
    }
    timerId = setInterval(() => show(current + 1), 3000);   // 3000ミリ秒 = 3秒ごと
    statusEl.textContent = '自動再生中';
};

const stop = () => {
    clearInterval(timerId);   // setInterval が返した番号を渡すと止まる
    timerId = null;
    statusEl.textContent = '一時停止中';
};

// マウスを乗せている間は止める（読んでいる途中で切り替わらないように）
slideshow.addEventListener('mouseenter', stop);
slideshow.addEventListener('mouseleave', start);

// キーボードでボタンにフォーカスしている間も止める
// focusin / focusout は、中の要素のフォーカスでも発生する（focus / blur は発生しない）
slideshow.addEventListener('focusin', stop);
slideshow.addEventListener('focusout', start);

show(0);

// 「動きを減らす」設定のユーザーには、自動再生をしない
if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    start();
} else {
    statusEl.textContent = '自動再生はオフです（動きを減らす設定）';
}
