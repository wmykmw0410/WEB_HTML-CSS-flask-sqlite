document.addEventListener('DOMContentLoaded', function () {
    const postalInput = document.getElementById('postal_code');
    const prefectureSelect = document.getElementById('prefecture');
    const cityInput = document.getElementById('city');
    const addressLineInput = document.getElementById('address_line');

    if (!postalInput || !prefectureSelect || !cityInput || !addressLineInput) {
        return;
    }

    postalInput.addEventListener('blur', function () {
        // ハイフンの有無を問わず、数字だけを取り出して7桁（日本の郵便番号の桁数）かを判定する
        const digits = postalInput.value.replace(/[^0-9]/g, '');
        if (digits.length !== 7) {
            return;
        }

        // zipcloud: APIキー不要・CORS対応の無料郵便番号検索API
        fetch(`https://zipcloud.ibsnet.co.jp/api/search?zipcode=${digits}`)
            .then(response => response.json())
            .then(data => {
                if (!data.results || data.results.length === 0) {
                    return;
                }
                const result = data.results[0];
                if (result.address1) {
                    prefectureSelect.value = result.address1;
                }
                cityInput.value = result.address2 || '';
                addressLineInput.value = result.address3 || '';
            })
            .catch(function () {
                // 通信エラー時は自動補完をあきらめ、手入力に任せる
            });
    });
});
