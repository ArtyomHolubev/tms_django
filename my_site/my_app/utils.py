from django.db import connection, reset_queries
import time
import functools


def query_debugger(logger):

    def wrapper(func):

        print("Hello from decorator!")

        @functools.wraps(func)
        def inner_func(*args, **kwargs):
            reset_queries()

            start_queries = len(connection.queries)

            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()

            end_queries = len(connection.queries)

            logger.debug(f"Function: {func.__name__}")
            logger.debug(f"Number of Queries: {end_queries - start_queries}")
            logger.debug(f"Finished in: {(end - start):.2f}s")

            return result

        return inner_func

    return wrapper
