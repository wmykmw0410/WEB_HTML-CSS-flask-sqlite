// --- 真偽の判定 ---
console.log(Boolean(''));          // Q1 予想：
console.log(Boolean('0'));         // Q2 予想：
console.log(Boolean([]));          // Q3 予想：
console.log(Boolean(null));        // Q4 予想：

// --- == と === ---
console.log(10 == '10');           // Q5 予想：
console.log(10 === '10');          // Q6 予想：

// --- 要素が見つからないとき ---
const el = document.getElementById('not-exist');
console.log(el);                   // Q7 予想：
console.log(Boolean(el));          // Q8 予想：

// --- 関数とコールバック ---
const double = (n) => n * 2;
console.log(typeof double);        // Q9 予想：
console.log(typeof double(5));     // Q10 予想：
