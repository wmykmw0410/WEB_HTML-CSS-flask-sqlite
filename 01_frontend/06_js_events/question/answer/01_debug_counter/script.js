// 解答1：バグを直したもの（3つのバグの説明は index.html のコメントを参照）

const textarea = document.getElementById('message');   // バグ2の修正：'messsage' → 'message'
const counter = document.getElementById('count');

textarea.addEventListener('input', () => {
    const length = textarea.value.length;               // バグ3の修正：lenght → length
    counter.textContent = length;
    counter.classList.toggle('over', length > 20);
});
