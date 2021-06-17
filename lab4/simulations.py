import random
from copy import copy, deepcopy
from pprint import pprint
from typing import List

from lab4.process import Process

PROCESSES_AMOUNT = 70
FRAME_AMOUNT = 150
MAX_FRAMES_PER_PROCESS = 5


def proportional(data: List[Process]):
    frame_cnt = FRAME_AMOUNT // PROCESSES_AMOUNT
    for proc in data:
        proc.assigned_pages = frame_cnt

    faults = 0
    for proc in data:
        if proc.is_faulted:
            faults += proc.overflow_amount
    print(f"Proportional faults: {faults}")


def random_s(data: List[Process]):
    for proc in data:
        proc.assigned_pages = random.randint(1, MAX_FRAMES_PER_PROCESS)
    faults = 0

    for proc in data:
        if proc.is_faulted:
            faults += proc.overflow_amount

    print(f"Random fault count: {faults}")


def priority(data: List[Process]):
    pages = copy(FRAME_AMOUNT)
    for proc in sorted(data):
        amount = min(pages, proc.pages)
        pages -= amount
        proc.assigned_pages = amount

    faults = 0
    for proc in data:
        if proc.is_faulted:
            faults += proc.overflow_amount

    print(f"Priority faults: {faults}")


def main():
    data = Process.gen_data(PROCESSES_AMOUNT, MAX_FRAMES_PER_PROCESS)

    proportional(deepcopy(data))
    random_s(deepcopy(data))
    priority(deepcopy(data))


if __name__ == '__main__':
    random.seed(1234567890)
    main()
