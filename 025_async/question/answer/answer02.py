"""
練習問題2：asyncio.gather の戻り値を使う — 解答
"""
import asyncio


async def fetch_square(n: int) -> int:
    """nを受け取り、0.1秒待ってから n の2乗を返す（重い処理のシミュレーション）"""
    await asyncio.sleep(0.1)
    return n * n


async def main() -> None:
    numbers = [1, 2, 3, 4, 5]

    results = await asyncio.gather(*(fetch_square(n) for n in numbers))

    print(f'入力: {numbers}')
    print(f'結果: {results}')

    assert results == [1, 4, 9, 16, 25]
    print('\n結果が正しい順番で取得できていることを確認しました。')


if __name__ == '__main__':
    asyncio.run(main())
