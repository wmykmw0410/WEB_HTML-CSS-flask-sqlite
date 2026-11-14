// TODO 1：const で userName を宣言し、'山田' を入れる


// TODO 2：let で score を宣言して 50 を入れ、そのあと 80 に書き換える（再代入）


// TODO 3：memo オブジェクトを作る（title は '会議'、pinned は false）。そのあと pinned を true に書き換える


// TODO 4：tags 配列を作る（'仕事' と '重要' の2つ）


// TODO 5：message に、テンプレートリテラルで「山田さんのタグは2個です」という文字を入れる
//         （'山田' と 2 は、userName と tags.length を使って埋め込む）


// ============================================================
// テスト（ここから下は書き換えない）
// ============================================================
// まだ書いていない（宣言されていない）変数や関数があっても、他のテストは続けて実行する
const get = (fn) => {
    try {
        return fn();
    } catch (error) {
        return '（未定義・エラー）';
    }
};

const check = (label, actual, expected) => {
    const ok = JSON.stringify(actual) === JSON.stringify(expected);
    if (ok) {
        console.log(`✅ ${label}`);
    } else {
        console.log(`❌ ${label}　結果：${JSON.stringify(actual)}　期待：${JSON.stringify(expected)}`);
    }
};

check('TODO 1：userName', get(() => userName), '山田');
check('TODO 2：score', get(() => score), 80);
check('TODO 3：memo.title', get(() => memo.title), '会議');
check('TODO 3：memo.pinned', get(() => memo.pinned), true);
check('TODO 4：tags', get(() => tags), ['仕事', '重要']);
check('TODO 5：message', get(() => message), '山田さんのタグは2個です');
