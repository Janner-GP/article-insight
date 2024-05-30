import time

def time_performance(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        print(f"La función {func.__name__} tardó {duration} segundos en ejecutarse.")
        return result
    return wrapper