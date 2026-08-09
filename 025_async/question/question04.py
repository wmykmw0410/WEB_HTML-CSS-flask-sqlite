"""
練習問題4：httpx.AsyncClient で複数の外部APIを同時に呼び出す

021_webapiでは requests（同期）でzipcloud APIを1件ずつ呼び出しました。
ここでは httpx.AsyncClient（非同期）を使い、複数の郵便番号を同時に検索します。

以下の TODO コメントの箇所にコードを書いて完成させてください。
実行方法: python question/question04.py

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

    # TODO: httpx.AsyncClient() を async with で開き、
    #       ZIP_CODES の各郵便番号について fetch_address(client, zip_code) を
    #       asyncio.gather で同時に実行して results に代入する
    results = []

    elapsed = time.perf_counter() - start

    for zip_code, data in zip(ZIP_CODES, results):
        info = data['results'][0]
        address = f"{info['address1']}{info['address2']}{info['address3']}"
        print(f'{zip_code} -> {address}')

    print(f'\n{len(ZIP_CODES)}件を同時に取得し、{elapsed:.2f}秒かかりました。')
    assert len(results) == len(ZIP_CODES)


if __name__ == '__main__':
    asyncio.run(main())
