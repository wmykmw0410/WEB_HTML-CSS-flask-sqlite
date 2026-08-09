"""
練習問題3：一部のタスクが失敗しても、他のタスクの結果を受け取る — 解答
"""
import asyncio


async def divide(a: int, b: int) -> float:
    await asyncio.sleep(0.1)
    return a / b   # b が 0 なら ZeroDivisionError


async def main() -> None:
    pairs = [(10, 2), (5, 0), (9, 3)]   # 2番目は0除算でエラーになる

    results = await asyncio.gather(
        *(divide(a, b) for a, b in pairs),
        return_exceptions=True,
    )

    successes = [r for r in results if not isinstance(r, Exception)]
    errors = [r for r in results if isinstance(r, Exception)]

    print(f'成功した結果: {successes}')
    print(f'失敗した件数: {len(errors)}')
    for e in errors:
        print(f'  エラー内容: {type(e).__name__}: {e}')

    assert successes == [5.0, 3.0]
    assert len(errors) == 1
    assert isinstance(errors[0], ZeroDivisionError)
    print('\n一部が失敗しても、成功した結果だけ取り出せることを確認しました。')


if __name__ == '__main__':
    asyncio.run(main())
