from functools import wraps
import logging
import time


def with_retry(retries=3, backoff=0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    time.sleep(backoff)
                    logging.error(f"An error occurred: {e}. Retrying...")
            raise Exception("Failed after multiple retries")

        return wrapper

    return decorator
