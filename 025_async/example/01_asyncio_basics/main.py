import time
import asyncio


# ---- 同期処理 ----
def sync_task(name: str) -> None:
    print(f"{name} Start")
    time.sleep(1)
    print(f"{name} End")


def run_sync_tasks() -> None:
    sync_task("Task1")
    sync_task("Task2")
    sync_task("Task3")


print("=== 同期処理 ===")
start = time.time()
run_sync_tasks()
print(f"経過時間: {time.time() - start:.2f}秒\n")


# ---- 非同期処理 ----
async def async_task(name: str) -> None:
    print(f"{name} Start")
    await asyncio.sleep(1)
    print(f"{name} End")


async def run_async_tasks() -> None:
    await asyncio.gather(
        async_task("TaskA"),
        async_task("TaskB"),
        async_task("TaskC"),
    )


print("=== 非同期処理 ===")
start = time.time()
asyncio.run(run_async_tasks())
print(f"経過時間: {time.time() - start:.2f}秒")
