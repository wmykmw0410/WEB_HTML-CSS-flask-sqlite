"""
練習問題2：asyncio.gather の戻り値を使う

asyncio.gather() は、渡した各タスクの戻り値を「渡した順番のリスト」として返します。

以下の TODO コメントの箇所にコードを書いて完成させてください。
実行方法: python question/question02.py
"""
import asyncio


async def fetch_square(n: int) -> int:
    """nを受け取り、0.1秒待ってから n の2乗を返す（重い処理のシミュレーション）"""
    await asyncio.sleep(0.1)
    return n * n


async def main() -> None:
    numbers = [1, 2, 3, 4, 5]

    # TODO: numbers の各要素について fetch_square() を呼び出し、
    #       asyncio.gather() で同時に実行して結果のリストを results に代入する
    #       ヒント: asyncio.gather(*(fetch_square(n) for n in numbers))
    results = []

    print(f'入力: {numbers}')
    print(f'結果: {results}')

    assert results == [1, 4, 9, 16, 25]
    print('\n結果が正しい順番で取得できていることを確認しました。')


if __name__ == '__main__':
    asyncio.run(main())
