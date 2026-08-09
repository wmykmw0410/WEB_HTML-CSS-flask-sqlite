"""
練習問題4：httpx.AsyncClient で複数の外部APIを同時に呼び出す — 解答

（インターネット接続が必要です）
"""
import asyncio
import time

import httpx

ZIP_CODES = ['7830060', '1000001', '5300001']


async def fetch_address(client: httpx.AsyncClient, zip_code: str) -> dict:
    res = await client.get(
        'https://zipcloud.ibsnet.co.jp/api/search',
        params={'zipcode': zip_code},
        timeout=10,
    )
    return res.json()


async def main() -> None:
    start = time.perf_counter()

    async with httpx.AsyncClient() as client:
        results = await asyncio.gather(*(fetch_address(client, z) for z in ZIP_CODES))

    elapsed = time.perf_counter() - start

    for zip_code, data in zip(ZIP_CODES, results):
        info = data['results'][0]
        address = f"{info['address1']}{info['address2']}{info['address3']}"
        print(f'{zip_code} -> {address}')

    print(f'\n{len(ZIP_CODES)}件を同時に取得し、{elapsed:.2f}秒かかりました。')
    assert len(results) == len(ZIP_CODES)


if __name__ == '__main__':
    asyncio.run(main())
