from multiprocessing import Pool
from time import time


def process_sum(a, b):
    return (a + b) * (b - a + 1) // 2


def calculate_sum(a, b, num_processes=8):
    step = (b - a + 1) // num_processes

    with Pool(processes=num_processes) as pool:
        tasks = []
        for i in range(num_processes):
            start = a + i * step
            if i == num_processes - 1:
                end = b
            else:
                end = a + (i + 1) * step - 1

            tasks.append((start, end))

        ress = pool.starmap(process_sum, tasks)

    return sum(ress)


if __name__ == '__main__':
    a, b = 1, 10000000000000
    start_time = time()
    print(f'processes: sum = {calculate_sum(a, b)}, time = {time() - start_time} s')
