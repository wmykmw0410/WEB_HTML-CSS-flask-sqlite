const header = document.getElementById('site-header');
const progress = document.getElementById('progress');
const toTop = document.getElementById('to-top');


// ============================================================
// 1. scroll イベント：スクロールした量に応じて表示を変える
// ============================================================
// window.scrollY：ページの一番上から、何px下までスクロールしたか
const onScroll = () => {
    const y = window.scrollY;

    // 少しでもスクロールしたら、ヘッダーに影を付ける
    header.classList.toggle('scrolled', y > 10);

    // 300px 以上スクロールしたら「トップへ戻る」ボタンを出す
    toTop.hidden = y < 300;

    // どこまで読んだか（0〜100%）を、バーの幅で表す
    //   スクロールできる最大の量 = ページ全体の高さ − 画面の高さ
    const max = document.documentElement.scrollHeight - window.innerHeight;
    const percent = max > 0 ? (y / max) * 100 : 0;
    progress.style.width = `${percent}%`;
};

// scroll イベントは、スクロール中に何度も（1秒に数十回）発生する。中の処理は軽くしておく
window.addEventListener('scroll', onScroll);
onScroll();   // 途中の位置で再読み込みされたときのために、最初にも1回呼んでおく


// ============================================================
// 2. JavaScript でスクロールさせる
// ============================================================
// window.scrollTo({ top: 位置, behavior: 'smooth' })：ページの指定した位置までスクロールする
toTop.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

// 要素.scrollIntoView({ behavior: 'smooth' })：その要素が見える位置までスクロールする
document.getElementById('jump-contact').addEventListener('click', () => {
    document.getElementById('contact').scrollIntoView({ behavior: 'smooth' });
});


// ============================================================
// 3. IntersectionObserver：要素が画面に入ったことを知る
// ============================================================
// scroll イベントで「要素が画面に入ったか」を毎回計算すると重くなる。
// IntersectionObserver を使うと、要素が画面に入った・出たときだけ、ブラウザが知らせてくれる
const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {                 // 画面に入った
            entry.target.classList.add('visible');
            observer.unobserve(entry.target);       // 一度表示したら、もう監視しない
        }
    });
}, {
    threshold: 0.2,   // 要素の20%が見えたら「入った」とみなす
});

document.querySelectorAll('.fade-in').forEach((el) => observer.observe(el));
