from asyncio import gather, run
from time import time


async def async_sum(a, b):
    return (a + b) * (b - a + 1) // 2


async def calculate_sum(a, b, num_tasks=8):
    step = (b - a + 1) // num_tasks
    tasks = []

    for i in range(num_tasks):
        start = a + i * step
        if i == num_tasks - 1:
            end = b
        else:
            end = a + (i + 1) * step - 1

        tasks.append(async_sum(start, end))

    ress = await gather(*tasks)
    return sum(ress)


if __name__ == '__main__':
    a, b = 1, 10000000000000
    start_time = time()
    print(f'async: sum = {run(calculate_sum(a, b))}, time = {time() - start_time} s')
