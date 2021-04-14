import inspect
from typing import Optional, Tuple

from lab2.read_request import ReadRequest, RequestQueue


def fifo(q: RequestQueue, previous_request: ReadRequest, read_head: int) -> Tuple[
        Optional[ReadRequest], int]:
    if previous_request:
        return previous_request, read_head
    s_queue = q.sort_by_toa()
    return None if len(s_queue) == 0 else s_queue[0], read_head


def sstf(q: RequestQueue, previous_request: ReadRequest, read_head: int) -> Tuple[
        Optional[ReadRequest], int]:
    if previous_request:
        return previous_request, read_head
    s_queue = q.sort_by_distance_to_read_head(read_head)
    return None if len(s_queue) == 0 else s_queue[0], read_head


class Scan:
    def __init__(self):
        self.direction = 0

    def toggle_direction(self):
        self.direction = 1 if self.direction == 0 else 0

    def __call__(self, q: RequestQueue, previous_request: ReadRequest, read_head: int) -> Tuple[
            Optional[ReadRequest], int]:
        if previous_request:
            return previous_request, read_head

        s_queue = q.sort_by_distance_with_cut_off(read_head, self.direction)

        if len(s_queue) == 0:
            self.toggle_direction()
            s_queue = q.sort_by_distance_with_cut_off(read_head, self.direction)

        if len(s_queue) == 0:
            return None, read_head

        return s_queue[0], read_head


class CScan:
    def __call__(self, q: RequestQueue, previous_request: ReadRequest, read_head: int) -> Tuple[
            Optional[ReadRequest], int]:
        if previous_request:
            return previous_request, read_head

        s_queue = q.sort_by_distance_with_cut_off(read_head, 0)

        if len(s_queue) == 0:
            read_head = 0
            s_queue = q.sort_by_distance_with_cut_off(0, 0)

        if len(s_queue) == 0:
            print("Not stonks")
            return None, read_head

        return s_queue[0], read_head


def edf(q: RequestQueue, previous_request: ReadRequest, read_head: int) -> Tuple[
        Optional[ReadRequest], int]:
    s_queue = q.sort_by_deadline()

    if q.is_empty():
        if previous_request is None:
            return None, read_head
        return previous_request, read_head

    if previous_request:
        if s_queue[0].deadline < previous_request.deadline:
            return s_queue[0], read_head
    return previous_request if previous_request else s_queue[0], read_head
