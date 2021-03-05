from typing import Optional

from utils.process import Process
from utils.queue import ProcessQueue


def fsfc_scheduler(queue: ProcessQueue, prev_proc: Process) -> Optional[Process]:
    if prev_proc is None:
        if not queue.is_empty():
            proc = queue.items[0]
            return proc
        return None
    else:
        return prev_proc
