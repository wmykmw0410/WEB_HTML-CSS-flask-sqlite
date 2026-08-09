import time
import asyncio
import httpx
import requests
from flask import Flask, jsonify, Response

app = Flask(__name__)

ZIP_CODES = ["1000001", "0600000", "9000000"]


# ---- 同期版：015_webapi と同じ requests を順番に呼ぶだけ ----
@app.get('/sync')
def get_addresses_sync() -> Response:
    start = time.time()
    results = []
    for zip_code in ZIP_CODES:
        res = requests.get("https://zipcloud.ibsnet.co.jp/api/search", params={"zipcode": zip_code})
        results.append(res.json())
    elapsed = time.time() - start
    return jsonify({"elapsed": round(elapsed, 2), "results": results})


# ---- 非同期版：httpx.AsyncClient + asyncio.gather で同時に呼ぶ ----
async def fetch_address(client: httpx.AsyncClient, zip_code: str) -> dict:
    res = await client.get("https://zipcloud.ibsnet.co.jp/api/search", params={"zipcode": zip_code})
    return res.json()


@app.get('/async')
async def get_addresses_async() -> Response:
    start = time.time()
    async with httpx.AsyncClient() as client:
        results = await asyncio.gather(*(fetch_address(client, z) for z in ZIP_CODES))
    elapsed = time.time() - start
    return jsonify({"elapsed": round(elapsed, 2), "results": results})


if __name__ == '__main__':
    app.run(debug=True, port=5071)
