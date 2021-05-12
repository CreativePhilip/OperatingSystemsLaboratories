import random
from typing import List

from lab3.utils import get_min_from_arr, least_used_in_the_future

MAX_PAGE_NUMBER = 20
REQUEST_AMOUNT = 100
MEM_CACHE_AMOUNT = 5

assert MAX_PAGE_NUMBER > MEM_CACHE_AMOUNT


def gen_page_requests() -> List[int]:
    return [random.randint(1, MAX_PAGE_NUMBER) for _ in range(REQUEST_AMOUNT)]


def fifo(data):
    cache = []
    cache_miss_count = 0
    last_idx = 0

    for r in data:
        if r not in cache:
            cache_miss_count += 1
            if len(cache) != MEM_CACHE_AMOUNT:
                cache.append(r)
            else:
                cache[last_idx] = r
                last_idx = (last_idx + 1) % MEM_CACHE_AMOUNT

    cache_miss_percent = int((cache_miss_count / REQUEST_AMOUNT) * 100)
    print(f"Fifo mem faults: {cache_miss_count} / {REQUEST_AMOUNT} -- {cache_miss_percent}%")


def opt(data):
    cache = []
    cache_miss_count = 0
    for idx, r in enumerate(data):
        if r not in cache:
            if len(cache) != MEM_CACHE_AMOUNT:
                cache.append(r)
            else:
                cache_miss_count += 1
                least_used = least_used_in_the_future(idx, data, cache)

                cache[cache.index(least_used)] = r

    cache_miss_percent = int((cache_miss_count / REQUEST_AMOUNT) * 100)
    print(f"OPT mem faults: {cache_miss_count} / {REQUEST_AMOUNT} -- {cache_miss_percent}%")


def rand(data):
    cache = []
    cache_miss_count = 0

    for r in data:
        if r not in cache:
            cache_miss_count += 1
            if len(cache) != MEM_CACHE_AMOUNT:
                cache.append(r)
            else:
                idx = random.randint(0, MEM_CACHE_AMOUNT - 1)
                cache[idx] = r

    cache_miss_percent = int((cache_miss_count / REQUEST_AMOUNT) * 100)
    print(f"RAND mem faults: {cache_miss_count} / {REQUEST_AMOUNT} -- {cache_miss_percent}%")


def lru(data):
    cache = []
    last_use_count = []
    cache_miss_count = 0
    for idx, r in enumerate(data):
        if r in cache:
            last_use_count[cache.index(r)] = idx
        else:
            if len(cache) != MEM_CACHE_AMOUNT:
                cache.append(r)
                last_use_count.append(idx)
            else:
                cache_miss_count += 1
                smallest = get_min_from_arr(last_use_count)
                item_idx = last_use_count.index(smallest)

                cache[item_idx] = r
                last_use_count[item_idx] = idx

    cache_miss_percent = int((cache_miss_count / REQUEST_AMOUNT) * 100)
    print(f"LRU mem faults: {cache_miss_count} / {REQUEST_AMOUNT} -- {cache_miss_percent}%")


def main():
    data = gen_page_requests()
    fifo(data)
    opt(data)
    lru(data)
    rand(data)


if __name__ == '__main__':
    random.seed(420)
    main()
