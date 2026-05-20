import asyncio
import time
import requests
from fastapi import FastAPI
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

app = FastAPI()

process_executor = ProcessPoolExecutor(max_workers=2)
thread_executor = ThreadPoolExecutor(max_workers=4)

URLS = [
    "https://httpbin.org/json",
    "https://httpbin.org/get",
    "https://httpbin.org/anything",
    "https://httpbin.org/delay/0.1",
    "https://httpbin.org/status/200",
]


def fetch_url(url: str) -> dict:
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.JSONDecodeError:
        return {"error": "Invalid JSON", "url": url, "text": response.text[:200]}
    except requests.exceptions.RequestException as e:
        return {"error": str(e), "url": url}


@app.get("/threads")
async def fetch_with_threads():
    start = time.perf_counter()
    loop = asyncio.get_running_loop()
    tasks = [loop.run_in_executor(thread_executor, fetch_url, url) for url in URLS]
    results = await asyncio.gather(*tasks)
    elapsed = time.perf_counter() - start
    return {
        "method": "threads",
        "elapsed_seconds": elapsed,
        "results_count": len(results),
    }


@app.get("/processes")
async def fetch_with_processes():
    start = time.perf_counter()
    loop = asyncio.get_running_loop()
    tasks = [loop.run_in_executor(process_executor, fetch_url, url) for url in URLS]
    results = await asyncio.gather(*tasks)
    elapsed = time.perf_counter() - start
    return {
        "method": "processes",
        "elapsed_seconds": elapsed,
        "results_count": len(results),
    }