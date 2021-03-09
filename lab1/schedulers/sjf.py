from typing import Optional

from utils.process import Process
from utils.queue import ProcessQueue, ProcessSorting


def sjf_non_preemptive(queue: ProcessQueue, prev_proc: Process) -> Optional[Process]:
    if prev_proc:
        return prev_proc

    if queue.is_empty():
        return None

    return queue.sort(ProcessSorting.ET)[0]


def sjf_preemptive(queue: ProcessQueue, prev_proc: Process) -> Optional[Process]:
    proc = queue.sort(ProcessSorting.ET)

    if queue.is_empty():
        return None

    if prev_proc is None:
        return proc[0]
    else:
        return prev_proc if prev_proc.execution_time_left <= proc[0].execution_time_left else proc[0]
