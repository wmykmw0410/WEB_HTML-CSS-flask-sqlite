// 解答4：目次付きの長い記事を、スクロールで読みやすくする

const progress = document.getElementById('progress');
const toTop = document.getElementById('to-top');
const sections = document.querySelectorAll('main section');
const tocLinks = document.querySelectorAll('.toc a');


// TODO 3・4：スクロールするたびに呼ばれる関数（中の処理は軽いものだけにする）
const onScroll = () => {
    const y = window.scrollY;

    // TODO 3：読了率。max が 0（スクロールできないほど短いページ）のときに 0 で割らないようにする
    const max = document.documentElement.scrollHeight - window.innerHeight;
    const percent = max > 0 ? Math.floor((y / max) * 100) : 100;
    progress.textContent = `読了 ${percent}%`;

    // TODO 4：400px 未満なら隠す
    toTop.hidden = y < 400;
};

window.addEventListener('scroll', onScroll);
onScroll();   // 途中の位置で再読み込みされたときのために、最初にも1回呼んでおく


// TODO 4：一番上へ戻る
toTop.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});


// TODO 5：今読んでいる節の目次に印を付ける
const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (!entry.isIntersecting) {
            return;   // 真ん中の線から出ていった節は無視する（入ってきた節の処理で印が付け替わる）
        }
        tocLinks.forEach((link) => {
            if (link.getAttribute('href') === `#${entry.target.id}`) {
                link.setAttribute('aria-current', 'true');
            } else {
                link.removeAttribute('aria-current');
            }
        });
    });
}, {
    rootMargin: '-50% 0px -50% 0px',   // 判定する範囲を「画面の上下の真ん中の線」だけにする
});

sections.forEach((section) => observer.observe(section));
