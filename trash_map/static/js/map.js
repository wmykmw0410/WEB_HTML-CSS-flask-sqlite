document.addEventListener('DOMContentLoaded', function () {
    const mapContainer = document.getElementById('map');
    const apiUrl = mapContainer.dataset.apiUrl;
    const focusId = mapContainer.dataset.focusId;

    const nearbyBtn = document.getElementById('nearbySearchBtn');
    const nearbyClearBtn = document.getElementById('nearbyClearBtn');
    const radiusSelect = document.getElementById('nearbyRadius');
    const statusEl = document.getElementById('nearbyStatus');
    const listPanel = document.getElementById('nearbyList');
    const listItemsEl = document.getElementById('nearbyListItems');

    const map = L.map('map', {
        minZoom: 5,
        maxBounds: [[20.0, 122.0], [46.0, 154.5]],
        maxBoundsViscosity: 1.0
    }).setView([35.681236, 139.767125], 15);

    L.tileLayer('https://cyberjapandata.gsi.go.jp/xyz/std/{z}/{x}/{y}.png', {
        attribution: '<a href="https://maps.gsi.go.jp/development/ichiran.html">地理院タイル</a>'
    }).addTo(map);

    let trashItems = [];
    // 周辺検索で表示/非表示を切り替えられるよう、idからマーカーを引けるようにしておく
    const markersById = new Map();
    let userMarker = null;

    function toRad(deg) {
        return deg * Math.PI / 180;
    }

    // 2点間の直線距離（メートル）をHaversine公式で計算する
    function distanceMeters(lat1, lng1, lat2, lng2) {
        const R = 6371000; // 地球の半径（メートル）
        const dLat = toRad(lat2 - lat1);
        const dLng = toRad(lng2 - lng1);
        const a = Math.sin(dLat / 2) ** 2 +
            Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLng / 2) ** 2;
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        return R * c;
    }

    function formatDistance(meters) {
        return meters >= 1000 ? `${(meters / 1000).toFixed(1)}km` : `${Math.round(meters)}m`;
    }

    function renderMarkers(items) {
        items.forEach(item => {
            const marker = L.marker([item.latitude, item.longitude]).addTo(map);
            marker.bindTooltip(item.name);
            marker.on('click', () => {
                window.location.href = `/trash/${item.id}`;
            });
            markersById.set(item.id, marker);

            // data-focus-id はHTMLのdata属性（常に文字列）なので、
            // item.id（数値）は String() で変換してから比較する
            if (focusId && String(item.id) === focusId) {
                map.setView([item.latitude, item.longitude], 17);
                marker.openTooltip();
            }
        });
    }

    function clearNearbySearch() {
        markersById.forEach(marker => {
            if (!map.hasLayer(marker)) {
                map.addLayer(marker);
            }
        });
        if (userMarker) {
            map.removeLayer(userMarker);
            userMarker = null;
        }
        listPanel.hidden = true;
        listItemsEl.innerHTML = '';
        statusEl.textContent = '';
    }

    function runNearbySearch(userLat, userLng) {
        const radius = Number(radiusSelect.value);

        if (userMarker) {
            map.removeLayer(userMarker);
        }
        userMarker = L.circleMarker([userLat, userLng], {
            radius: 8,
            color: '#1976d2',
            fillColor: '#1976d2',
            fillOpacity: 0.8
        }).addTo(map).bindTooltip('現在地');

        const nearby = trashItems
            .map(item => ({
                item: item,
                distance: distanceMeters(userLat, userLng, item.latitude, item.longitude)
            }))
            .filter(entry => entry.distance <= radius)
            .sort((a, b) => a.distance - b.distance);

        // 新しいAPIは呼ばず、既に取得済みのマーカーを表示/非表示切り替えするだけにする
        const nearbyIds = new Set(nearby.map(entry => entry.item.id));
        markersById.forEach((marker, id) => {
            const isNearby = nearbyIds.has(id);
            if (isNearby && !map.hasLayer(marker)) {
                map.addLayer(marker);
            } else if (!isNearby && map.hasLayer(marker)) {
                map.removeLayer(marker);
            }
        });

        listItemsEl.innerHTML = '';
        if (nearby.length === 0) {
            statusEl.textContent = `半径${formatDistance(radius)}以内にゴミ箱は見つかりませんでした。`;
            listPanel.hidden = true;
            map.setView([userLat, userLng], 16);
            return;
        }

        statusEl.textContent = `${nearby.length}件見つかりました。`;
        nearby.forEach(entry => {
            const li = document.createElement('li');
            const a = document.createElement('a');
            a.href = `/trash/${entry.item.id}`;
            a.textContent = `${entry.item.name}（${formatDistance(entry.distance)}）`;
            li.appendChild(a);
            listItemsEl.appendChild(li);
        });
        listPanel.hidden = false;

        const bounds = L.latLngBounds(nearby.map(entry => [entry.item.latitude, entry.item.longitude]));
        bounds.extend([userLat, userLng]);
        map.fitBounds(bounds, { padding: [40, 40] });
    }

    nearbyBtn.addEventListener('click', () => {
        if (!navigator.geolocation) {
            statusEl.textContent = 'このブラウザは現在地取得に対応していません。';
            return;
        }
        statusEl.textContent = '現在地を取得中...';
        navigator.geolocation.getCurrentPosition(
            position => {
                runNearbySearch(position.coords.latitude, position.coords.longitude);
            },
            () => {
                statusEl.textContent = '現在地を取得できませんでした。';
            }
        );
    });

    nearbyClearBtn.addEventListener('click', clearNearbySearch);

    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            trashItems = data.items;
            renderMarkers(trashItems);
        });
});
