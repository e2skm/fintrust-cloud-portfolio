"""
Python Concurrency - Threading, Asyncio, and When to Use Each
Generated from training material.
"""

import time
import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed

# ====================================================
# A01 - Concurrency Models Notes
# ====================================================
# Threading: Best for I/O-bound work
# Asyncio: Best for very high concurrency I/O
# Multiprocessing: Best for CPU-bound work


# ====================================================
# A02 - ThreadPoolExecutor Example
# ====================================================

def get_object_metadata(bucket: str, key: str) -> dict:
    """Simulated S3 metadata lookup."""
    time.sleep(0.1)
    return {"key": key, "size": 1024}


def threaded_metadata_lookup():
    keys = [f"data/file{i}.csv" for i in range(1, 6)]
    bucket = "fintrust-raw-data"

    results = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {
            executor.submit(get_object_metadata, bucket, key): key
            for key in keys
        }

        for future in as_completed(futures):
            try:
                results.append(future.result())
            except Exception as e:
                print(f"Failed for {futures[future]}: {e}")

    return results


# ====================================================
# A03 - Asyncio Example
# ====================================================

async def fetch_account_data(account_id: int) -> dict:
    await asyncio.sleep(0.1)
    return {"account_id": account_id, "status": "success"}


async def fetch_all_accounts(account_ids: list[int]):
    tasks = [fetch_account_data(account_id) for account_id in account_ids]
    return await asyncio.gather(*tasks, return_exceptions=True)


# ====================================================
# A04 - Exercise Solution
# FinTrust Nightly Pipeline Benchmark
# ====================================================

def query_dynamodb_table(table_name: str):
    time.sleep(0.2)
    return f"Data from {table_name}"


def sequential_queries(tables):
    start = time.perf_counter()
    results = [query_dynamodb_table(table) for table in tables]
    elapsed = time.perf_counter() - start
    return results, elapsed


def parallel_queries(tables):
    start = time.perf_counter()

    with ThreadPoolExecutor(max_workers=20) as executor:
        results = list(executor.map(query_dynamodb_table, tables))

    elapsed = time.perf_counter() - start
    return results, elapsed


def benchmark():
    tables = [f"table_{i}" for i in range(1, 41)]

    _, sequential_time = sequential_queries(tables)
    _, parallel_time = parallel_queries(tables)

    speedup = sequential_time / parallel_time

    print(f"Sequential Time: {sequential_time:.2f}s")
    print(f"Parallel Time:   {parallel_time:.2f}s")
    print(f"Speedup Factor:  {speedup:.2f}x")


if __name__ == '__main__':
    print('Threading Example:')
    print(threaded_metadata_lookup())

    print('
Asyncio Example:')
    print(asyncio.run(fetch_all_accounts(list(range(1, 11)))))

    print('
Benchmark:')
    benchmark()
