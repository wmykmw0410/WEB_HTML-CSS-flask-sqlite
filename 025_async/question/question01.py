"""
練習問題1：asyncio.gather で複数のタスクを同時実行し、所要時間を比較する

以下の TODO コメントの箇所にコードを書いて完成させてください。

やること:
  1. 0.5秒 sleep するタスクを3つ、順番に実行（直列）した場合の所要時間を計測する
  2. 同じ3つのタスクを asyncio.gather で同時実行（並列）した場合の所要時間を計測する
  3. 並列実行の方が速いことを表示で確認する

実行方法: python question/question01.py
"""
import asyncio
import time


async def sleep_task(name: str, seconds: float) -> None:
    print(f'{name} start')
    await asyncio.sleep(seconds)
    print(f'{name} end')


async def run_sequential() -> float:
    start = time.perf_counter()
    # TODO: sleep_task('A', 0.5) → sleep_task('B', 0.5) → sleep_task('C', 0.5) を
    #       await で1つずつ順番に実行する
    return time.perf_counter() - start


async def run_concurrent() -> float:
    start = time.perf_counter()
    # TODO: asyncio.gather() で sleep_task('A', 0.5)・('B', 0.5)・('C', 0.5) を
    #       同時に実行する
    return time.perf_counter() - start


async def main() -> None:
    print('=== 直列実行 ===')
    sequential_time = await run_sequential()
    print(f'経過時間: {sequential_time:.2f}秒\n')

    print('=== 並列実行 ===')
    concurrent_time = await run_concurrent()
    print(f'経過時間: {concurrent_time:.2f}秒')

    # 直列なら約1.5秒、並列なら約0.5秒かかるはず
    assert sequential_time > 1.0, 'run_sequential が実装されていません'
    assert concurrent_time > 0.3, 'run_concurrent が実装されていません'
    assert concurrent_time < sequential_time, '並列実行の方が速くなるはずです'
    print('\n並列実行の方が速いことを確認しました。')


if __name__ == '__main__':
    asyncio.run(main())
