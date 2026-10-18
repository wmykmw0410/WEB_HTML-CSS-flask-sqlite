const textarea = document.getElementById('messsage');
const counter = document.getElementById('count');

textarea.addEventListener('input', () => {
    const length = textarea.value.lenght;
    counter.textContent = length;
    counter.classList.toggle('over', length > 20);
});
