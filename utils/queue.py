from copy import copy
from enum import Enum
from typing import List

from utils.process import Process
from pprint import pprint

from rich.console import Console
from rich.table import Table


class ProcessSorting(Enum):
    NONE = "name"
    TOA = "time_of_arrival"
    ET = "execution_time_left"


class ProcessQueue:
    def __init__(self, arr=None):
        self.items: List[Process] = [] if arr is None else arr

    def pop(self, item: Process):
        self.items.remove(item)

    def get_scheduled(self, global_timer) -> "ProcessQueue":
        return ProcessQueue(list(filter(lambda x: x.can_execute(global_timer), self.sort())))

    def get_flat_execution_time(self):
        result = 0
        for i in self.items:
            result += i.execution_time
        return copy(result)

    def sort(self, sorting=ProcessSorting.NONE):
        return sorted(self.items, key=lambda x: getattr(x, sorting.value))

    def is_empty(self):
        return len(self.items) == 0

    def fill_randomly(self, n, min_execution_time, max_execution_time, max_time_of_arrival):
        for i in range(n):
            self.items.append(Process.create_random(f"{i:0{len(str(n))}}",
                                                    min_execution_time=min_execution_time,
                                                    max_execution_time=max_execution_time,
                                                    max_time_of_arrival=max_time_of_arrival))

    def print(self):
        pprint(self.items)

    def table(self, sorting=ProcessSorting.NONE):
        tab = Table(title=f"ProcessQueue  Sorted by: {sorting.value}", style="bold", title_style="bold magenta")

        tab.add_column("Name", justify="right", style="cyan")
        tab.add_column("Time of arrival", justify="right", style="bold green")
        tab.add_column("Execution time", justify="right", style="bold green")

        for proc in self.sort(sorting):
            tab.add_row(proc.name,
                        str(proc.time_of_arrival),
                        str(proc.execution_time))

        return tab
