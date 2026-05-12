from threading import Thread
from time import time


def thread_sum(a, b, res, i):
    res[i] = (a + b) * (b - a + 1) // 2


def calculate_sum(a, b, num_threads=8):
    step = (b - a + 1) // num_threads
    threads = []
    ress = [0 for i in range(num_threads)]

    for i in range(num_threads):
        start = a + i * step
        if i == num_threads - 1:
            end = b
        else:
            end = a + (i + 1) * step - 1

        t = Thread(target=thread_sum, args=(start, end, ress, i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return sum(ress)


if __name__ == '__main__':
    a, b = 1, 10000000000000
    start_time = time()
    print(f'threads: sum = {calculate_sum(a, b)}, time = {time() - start_time} s')
