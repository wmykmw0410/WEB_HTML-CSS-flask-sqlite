// ============================================================
// 1. popover 属性のポップアップ（メニュー・ヘルプ）
// ============================================================
// HTML の popovertarget だけで開閉できるので、JavaScript は不要。
// 開いた・閉じたときに何かしたい場合は toggle イベントを使う
const menu = document.getElementById('menu');
menu.addEventListener('toggle', (event) => {
    console.log(`メニューが ${event.newState === 'open' ? '開きました' : '閉じました'}`);
});


// ============================================================
// 2. JavaScript で開閉するポップアップ（自動で消える通知）
// ============================================================
const toast = document.getElementById('toast');
let hideTimer = null;

document.getElementById('save').addEventListener('click', () => {
    // 本来はここで保存処理をする

    toast.showPopover();   // 開く（popover="manual" なので、外側をクリックしても閉じない）

    // 連続で押されたときに、前のタイマーで早く消えてしまわないよう、前のタイマーを取り消す
    clearTimeout(hideTimer);
    // setTimeout(関数, ミリ秒)：指定した時間のあとに1回だけ関数を呼ぶ
    hideTimer = setTimeout(() => {
        toast.hidePopover();   // 閉じる
    }, 3000);
});

// 補足：ポップアップとモーダルウィンドウの違い
//   ポップアップ（popover）      ：後ろの画面も操作できる。外側をクリックすると閉じる（メニュー・ヘルプ・通知）
//   モーダルウィンドウ（<dialog> の showModal()）：閉じるまで後ろの画面は操作できない（確認・詳細表示・入力）
//   → 03_modal を参照
