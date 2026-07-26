# Error Handling and Logging Reference / Mini Lesson
# ==================================================
#
# This file preserves the original reference content and expands it into a
# runnable, educational Python reference. Read through the comments and run
# the examples to learn practical error handling and logging techniques.
#
# ---------------------------------------------------------------------------
# ORIGINAL REFERENCE CONTENT (PRESERVED)
# ---------------------------------------------------------------------------

# try / except / else / finally — Structure Cheatsheet
#
# try:
#     # Code that might fail
#     result = risky_operation()
# except SpecificError as e:
#     # Handle a specific exception type
#     handle(e)
# except (TypeError, ValueError) as e:
#     # Handle multiple types the same way
#     handle(e)
# except Exception as e:
#     # Catch-all for unexpected errors — log and optionally re-raise
#     logger.exception("Unexpected: %s", e)
#     raise
# else:
#     # Runs ONLY if no exception occurred
#     use(result)
# finally:
#     # Runs ALWAYS — use for cleanup
#     cleanup()
#
# Rules:
# try      -> Always contains code that might fail
# except   -> Runs when matching exception is raised
# else     -> Runs only if no exception occurred
# finally  -> Always runs, even during exceptions
#
# Exception Types Reference
# FileNotFoundError, PermissionError, ValueError, KeyError,
# IndexError, TypeError, AttributeError, JSONDecodeError,
# UnicodeDecodeError, OSError, ZeroDivisionError
#
# Exception Hierarchy (simplified)
# BaseException
# ├── SystemExit
# ├── KeyboardInterrupt
# └── Exception
#     ├── OSError
#     ├── ValueError
#     ├── TypeError
#     ├── KeyError
#     ├── IndexError
#     └── AttributeError

import json
import logging
from pathlib import Path
from contextlib import contextmanager

# ---------------------------------------------------------------------------
# LOGGING CONFIGURATION
# ---------------------------------------------------------------------------

LOG_DIR = Path('logs')
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(name)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(LOG_DIR / 'app.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('reference.error_handling')

# ---------------------------------------------------------------------------
# EXAMPLE 1: try / except / else / finally
# ---------------------------------------------------------------------------

def divide_numbers(numerator: float, denominator: float) -> float:
    try:
        result = numerator / denominator
    except ZeroDivisionError as exc:
        logger.error('Cannot divide by zero: %s', exc)
        raise
    else:
        logger.info('Division successful.')
        return result
    finally:
        logger.debug('divide_numbers() finished execution.')

# ---------------------------------------------------------------------------
# EXAMPLE 2: SAFE TYPE CONVERSION
# ---------------------------------------------------------------------------

def safe_int_conversion(value: str):
    try:
        return int(value)
    except ValueError as exc:
        logger.warning('Invalid integer value: %s', value)
        logger.debug('Conversion detail: %s', exc)
        return None

# ---------------------------------------------------------------------------
# EXAMPLE 3: FILE HANDLING
# ---------------------------------------------------------------------------

def read_text_file(file_path: str) -> str | None:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        logger.error('File not found: %s', file_path)
    except PermissionError:
        logger.error('Permission denied: %s', file_path)
    return None

# ---------------------------------------------------------------------------
# EXAMPLE 4: JSON HANDLING
# ---------------------------------------------------------------------------

def load_json(json_text: str):
    try:
        return json.loads(json_text)
    except json.JSONDecodeError as exc:
        logger.error('Invalid JSON: %s', exc)
        return None

# ---------------------------------------------------------------------------
# EXAMPLE 5: CUSTOM EXCEPTIONS
# ---------------------------------------------------------------------------

class InvalidAgeError(Exception):
    """Raised when age validation fails."""


def validate_age(age: int) -> None:
    if age < 0:
        raise InvalidAgeError('Age cannot be negative.')

# ---------------------------------------------------------------------------
# EXAMPLE 6: CONTEXT MANAGER PATTERN
# ---------------------------------------------------------------------------

class MockConnection:
    def rollback(self):
        logger.info('Rollback executed.')

    def close(self):
        logger.info('Connection closed.')


@contextmanager
def managed_connection():
    conn = MockConnection()
    try:
        yield conn
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

# ---------------------------------------------------------------------------
# EXAMPLE 7: LOGGING LEVELS
# ---------------------------------------------------------------------------

def demonstrate_logging_levels():
    logger.debug('Debug message')
    logger.info('Info message')
    logger.warning('Warning message')
    logger.error('Error message')
    logger.critical('Critical message')

# ---------------------------------------------------------------------------
# BEST PRACTICES
# ---------------------------------------------------------------------------
# 1. Catch the most specific exception possible.
# 2. Avoid bare except clauses.
# 3. Use logger.exception() inside exception handlers.
# 4. Do not silently ignore errors.
# 5. Re-raise exceptions when they cannot be handled.
# 6. Use finally blocks for cleanup.
# 7. Prefer context managers for resources.
# 8. Log useful context, not just the error message.

# ---------------------------------------------------------------------------
# DEMONSTRATION
# ---------------------------------------------------------------------------

def main():
    logger.info('Starting demo.')

    safe_int_conversion('123')
    safe_int_conversion('abc')

    try:
        divide_numbers(10, 0)
    except ZeroDivisionError:
        logger.info('ZeroDivisionError handled in main().')

    load_json('{bad json}')

    try:
        validate_age(-2)
    except InvalidAgeError as exc:
        logger.warning('Validation failed: %s', exc)

    with managed_connection():
        logger.info('Using managed connection.')

    demonstrate_logging_levels()

    logger.info('Demo complete.')


if __name__ == '__main__':
    main()
