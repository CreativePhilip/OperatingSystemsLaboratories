from typing import Optional

from utils.process import Process
from utils.queue import ProcessQueue, ProcessSorting


def fsfc_scheduler(queue: ProcessQueue, prev_proc: Process) -> Optional[Process]:
    if prev_proc:
        return prev_proc

    if queue.is_empty():
        return None

    return queue.sort(ProcessSorting.TOA)[0]
