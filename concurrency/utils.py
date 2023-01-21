import time


def timer(fun):
    def _measure_time(*args, **kwargs):
        t0 = time.time()
        result = fun(*args, **kwargs)
        print(f'Execution took {time.time() - t0:.2f} seconds')
        return result

    return _measure_time
