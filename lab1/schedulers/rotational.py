from typing import Optional

from utils.process import Process
from utils.queue import ProcessQueue


class Rotational:
    def __init__(self):
        self.seen_nodes = []

    def __call__(self, queue: ProcessQueue, prev_proc: Process) -> Optional[Process]:
        if len(queue.items) == 0:
            return None

        for proc in queue.items:
            if proc in self.seen_nodes:
                continue

            self.seen_nodes.append(proc)
            return proc
        else:
            self.seen_nodes.clear()
            return self(queue, prev_proc)
