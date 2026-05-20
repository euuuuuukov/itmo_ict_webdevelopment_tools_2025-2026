import asyncio
import time
from fastapi import FastAPI
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

app = FastAPI()

process_executor = ProcessPoolExecutor(max_workers=4)
thread_executor = ThreadPoolExecutor(max_workers=4)


def sum_sq(n: int) -> int:
    result = 1
    for i in range(2, n + 1):
        result += i ** 2
    return result


@app.get("/threads")
async def cpu_with_threads(n: int = 200000):
    loop = asyncio.get_running_loop()
    start = time.perf_counter()
    result = await loop.run_in_executor(thread_executor, sum_sq, n)
    elapsed = time.perf_counter() - start
    return {
        "method": "threads",
        "elapsed_seconds": elapsed,
        "result": result
    }


@app.get("/processes")
async def cpu_with_processes(n: int = 200000):
    loop = asyncio.get_running_loop()
    start = time.perf_counter()
    result = await loop.run_in_executor(process_executor, sum_sq, n)
    elapsed = time.perf_counter() - start
    return {
        "method": "processes",
        "elapsed_seconds": elapsed,
        "result": result
    }
