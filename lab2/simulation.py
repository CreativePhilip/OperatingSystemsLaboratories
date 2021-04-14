import random
from typing import Callable, Optional, Tuple, Type

from statistics import mean

from lab2.algos import fifo, sstf, Scan, CScan, edf
from lab2.read_request import RequestQueue, ReadRequest
from lab2.stats import Stats

ALGO_LAMBDA: Type = Callable[[RequestQueue, ReadRequest, int], Tuple[Optional[ReadRequest], int]]


class Simulation:
    def __init__(self, queue: RequestQueue, algo: ALGO_LAMBDA):
        self.stat = Stats()
        self.algo = algo
        self.queue = queue
        self.delays = []

        self.tick = 0
        self.read_head = 0

    def simulate(self):
        request = None
        while not self.queue.is_empty():
            request, self.read_head = self.algo(self.queue.get_active(self.tick), request, self.read_head)
            if request:
                self.read_head = request.tick(self.read_head, self.tick)
                self.stat.tick_position(self.read_head)

                if request.is_done:
                    self.queue.remove(request)
                    self.delays.append(request.fetch_time)
                    request = None

            assert 0 <= self.read_head
            assert self.read_head <= ReadRequest.MAX_DISK_SIZE

            self.tick += 1

        print(f"Tick count {self.tick}")
        print(f"{mean(self.delays)}")
        self.stat.show()


if __name__ == '__main__':
    random.seed(1234)
    q = ReadRequest.create_list(200)
    # s = Simulation(q, fifo)
    # s = Simulation(q, sstf)
    # s = Simulation(q, Scan())
    s = Simulation(q, CScan())
    # s = Simulation(q, edf)
    s.simulate()
