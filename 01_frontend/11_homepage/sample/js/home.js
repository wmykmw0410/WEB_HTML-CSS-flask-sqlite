/*
home.js：ホーム（index.html）の動き

    作品のスライドショー … data/works.json を fetch して（10_js_data 2節）、スライドを作る（09_js_ui 4節）
*/

const slideshow = document.getElementById('slideshow');
const slidesArea = document.getElementById('slides');
const dotsArea = document.getElementById('dots');
const slidesStatus = document.getElementById('slides-status');

let slides = [];
let dots = [];
let current = 0;
let timerId = null;


// n 枚目を表示する（範囲外の番号は回り込ませる）
const show = (n) => {
    current = (n + slides.length) % slides.length;
    slides.forEach((slide, index) => slide.classList.toggle('active', index === current));
    dots.forEach((dot, index) => dot.classList.toggle('current', index === current));
};

// 自動再生（5秒ごと）
const startAuto = () => {
    if (timerId !== null || window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        return;
    }
    timerId = setInterval(() => show(current + 1), 5000);
};

const stopAuto = () => {
    clearInterval(timerId);
    timerId = null;
};


// 作品1件分のスライドを作る
const createSlide = (work, index) => {
    const slide = document.createElement('a');
    slide.className = 'slide';
    slide.href = 'works.html';
    slide.style.setProperty('--slide-hue', `${(index * 70 + 160) % 360}`);   // 作品ごとに色を変える

    const title = document.createElement('strong');
    title.textContent = work.title;

    const description = document.createElement('span');
    description.textContent = work.description;

    slide.append(title, description);
    return slide;
};


const loadSlides = async () => {
    try {
        const response = await fetch('data/works.json');
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        const works = await response.json();

        // 新しい順に3件だけをスライドにする
        works.slice(0, 3).forEach((work, index) => {
            slidesArea.append(createSlide(work, index));

            const dot = document.createElement('button');
            dot.type = 'button';
            dot.addEventListener('click', () => show(index));
            dotsArea.append(dot);
        });

        slides = Array.from(slidesArea.children);
        dots = Array.from(dotsArea.children);
        slidesStatus.textContent = '';
        show(0);
        startAuto();
    } catch (error) {
        slidesStatus.textContent = '作品の読み込みに失敗しました。';
        slidesStatus.classList.add('error');
        console.error(error);
    }
};


if (slideshow) {
    slideshow.querySelector('.prev').addEventListener('click', () => show(current - 1));
    slideshow.querySelector('.next').addEventListener('click', () => show(current + 1));

    // マウスを乗せている間・フォーカスがある間は止める
    slideshow.addEventListener('mouseenter', stopAuto);
    slideshow.addEventListener('mouseleave', startAuto);
    slideshow.addEventListener('focusin', stopAuto);
    slideshow.addEventListener('focusout', startAuto);

    loadSlides();
}
