import functools
import logging

def debug(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)

        logging.debug(f"Calling: {func.__name__}({signature})")

        try:
            result = func(*args, **kwargs)
            logging.debug(f"{func.__name__} returned {result!r}")
            return result
        except Exception as e:
            logging.exception(f"Exception raised in {func.__name__}. {str(e)}")
            raise

    return wrapper
