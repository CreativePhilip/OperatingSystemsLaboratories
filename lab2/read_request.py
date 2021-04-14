from random import randint
from typing import List, Optional


class ReadRequest:
    MAX_DISK_SIZE = 100
    MAX_TOA = 10000

    AMOUNT = 0

    def __init__(self, toa: int, location: int, deadline=0):
        self.toa = toa
        self.location = location
        self.deadline = self.toa + deadline

        self.fetch_time = None
        self.idx = ReadRequest.AMOUNT
        ReadRequest.AMOUNT += 1

    def tick(self, head_pos: int, tick: int):
        # Required because in the case that we change requests and the new one is exactly
        # on the current position, we would fail the bounds assertion in simulation.py
        if head_pos == self.location:
            self.fetch_time = tick - self.toa
            return head_pos

        direction = 1 if self.location > head_pos else -1
        new_head = head_pos + direction
        # print(f"{self.idx}.tick(head: {head_pos}, loc: {self.location})")
        if new_head == self.location:
            self.fetch_time = tick - self.toa

        return new_head

    @property
    def is_done(self):
        return self.fetch_time is not None

    def __eq__(self, other: "ReadRequest"):
        if not self.__class__ == other.__class__:
            return False

        return self.toa == other.toa and self.location == other.location

    def __str__(self):
        return f"ReadRequest(toa={self.toa}, location={self.location})"

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def create_list(n: int) -> "RequestQueue":
        queue = RequestQueue([])
        for _ in range(n):
            queue.append(ReadRequest.get_random())
        return queue

    @classmethod
    def get_random(cls):
        return cls(
            toa=randint(0, cls.MAX_TOA),
            location=randint(0, cls.MAX_DISK_SIZE),
            deadline=randint(0, cls.MAX_TOA))


class RequestQueue:
    def __init__(self, data: List[ReadRequest]):
        self.data = data
        self.fd_scan_target: Optional[ReadRequest] = None

    def append(self, item: ReadRequest):
        return self.data.append(item)

    def remove(self, item: ReadRequest):
        return self.data.remove(item)

    def is_empty(self):
        return len(self.data) == 0

    def sort_by_toa(self):
        return sorted(self.data, key=lambda x: x.toa)

    def sort_by_distance_to_read_head(self, read_head: int):
        return sorted(self.data, key=lambda x: abs(x.location - read_head))

    def sort_by_distance_with_cut_off(self, read_head: int, direction: int):
        def filter_func(item: ReadRequest) -> bool:
            if direction == 0:
                return item.location >= read_head
            return item.location <= read_head

        return sorted(list(filter(filter_func, self.data)), key=lambda x: abs(x.location - read_head))

    def sort_by_deadline(self):
        return sorted(self.data, key=lambda x: x.deadline)

    def sort_by_fd_deadline(self, read_head: int):
        def filter_func(item: ReadRequest):
            return read_head <= item.location

        if self.fd_scan_target not in self.data:
            self.fd_scan_target = None

        if self.fd_scan_target is None:
            self.fd_scan_target = self.sort_by_deadline()[0]
        filtered = list(filter(filter_func, self.data))

    def get_active(self, tick: int):
        new_queue = RequestQueue([])
        for request in self.data:
            if request.toa <= tick:
                new_queue.append(request)

        return new_queue

    def __str__(self):
        return self.data.__str__()

    def __repr__(self):
        return self.data.__repr__()


if __name__ == '__main__':
    q = RequestQueue([
        ReadRequest(toa=0, location=0),
        ReadRequest(toa=0, location=10),
        ReadRequest(toa=0, location=20),
        ReadRequest(toa=0, location=30),
        ReadRequest(toa=0, location=40),
        ReadRequest(toa=0, location=50),
        ReadRequest(toa=0, location=60),
        ReadRequest(toa=0, location=70),
        ReadRequest(toa=0, location=80),
        ReadRequest(toa=0, location=90),
        ReadRequest(toa=0, location=100),
    ])

    print(q.sort_by_distance_with_cut_off(80, 0))
