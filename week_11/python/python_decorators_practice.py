"""
Python Decorators - Functions That Wrap Functions
Generated from training material.
"""

from functools import wraps
import logging
import time

logging.basicConfig(level=logging.INFO)

# ====================================================
# A01 - Timer Decorator
# ====================================================

def timer(func):
    """Decorator that logs execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} completed in {elapsed:.3f}s")
        return result
    return wrapper


@timer
def load_data(table_name: str) -> list:
    time.sleep(0.5)
    return []


# ====================================================
# A02 - Retry Decorator
# ====================================================

def retry(max_attempts=3, delay_seconds=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    wait = delay_seconds * (2 ** attempt)
                    logging.warning(
                        f"Attempt {attempt + 1}/{max_attempts} failed: {e}. Retrying in {wait}s"
                    )
                    time.sleep(wait)
            raise last_error
        return wrapper
    return decorator


@retry(max_attempts=3, delay_seconds=1)
def fetch_from_api(endpoint: str) -> dict:
    raise ConnectionError("Temporary API failure")


# ====================================================
# A03 - Decorator With Arguments
# ====================================================

def validate_types(**expected_types):
    def decorator(func):
        @wraps(func)
        def wrapper(**kwargs):
            for param, expected in expected_types.items():
                if param in kwargs and not isinstance(kwargs[param], expected):
                    raise TypeError(
                        f"'{param}' must be {expected.__name__}, got {type(kwargs[param]).__name__}"
                    )
            return func(**kwargs)
        return wrapper
    return decorator


@validate_types(account_id=int, amount=float)
def process_transaction(account_id: int, amount: float) -> bool:
    return amount > 0


# ====================================================
# Exercise 1 - Logging Decorator
# ====================================================

def log_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"Calling {func.__name__} args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        logging.info(f"{func.__name__} returned {result}")
        return result
    return wrapper


@log_call
def load_csv(path: str):
    return f"Loaded file: {path}"


# ====================================================
# Exercise 2 - Memoize Decorator
# ====================================================

def memoize(func):
    cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    return wrapper


@memoize
def slow_database_query(query: str):
    time.sleep(2)
    return f"Results for: {query}"


# ====================================================
# Exercise 3 - Stacking Decorators
# ====================================================

@timer
@retry(max_attempts=2, delay_seconds=1)
def unstable_job():
    raise RuntimeError("Job failed")


if __name__ == '__main__':
    load_data('transactions')
    load_csv('transactions.csv')
    print(process_transaction(account_id=1, amount=100.0))
    print(slow_database_query('SELECT * FROM transactions'))
