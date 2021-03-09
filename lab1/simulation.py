from typing import Callable, Optional, Type

from lab1.schedulers import SchedulerStatistics
from utils.process import Process
from utils.queue import ProcessQueue

from rich.console import Console
from rich.table import Table


SchedulerType: Type = Callable[[ProcessQueue, Process], Optional[Process]]


class Simulation:
    def __init__(self, queue: ProcessQueue, scheduler: SchedulerType, name="Simm"):
        self.q = queue
        self.scheduler = scheduler
        self.stats = SchedulerStatistics()
        self.flat_time = self.q.get_flat_execution_time()
        self.name = name
        self.global_timer = 0

    def simulate(self):
        current_process: Optional[Process] = None
        while not self.q.is_empty():
            scheduled_processes = self.q.get_scheduled(self.global_timer)
            current_process = self.scheduler(scheduled_processes, current_process)

            if current_process:
                current_process.tick(self.global_timer)

                if current_process.start_time == self.global_timer:
                    self.stats.waiting_times.append(current_process.start_time - current_process.time_of_arrival)

                if current_process.is_finished():
                    self.stats.exec_waiting_times.append(current_process.execution_waiting_time)
                    self.q.pop(current_process)

                    current_process = None

            self.global_timer += 1

    def report(self):
        tab = Table(title=self.name, style="bold", title_style="bold magenta")
        tab.add_column("key", justify="right", style="cyan")
        tab.add_column("value", justify="left", style="bold green")

        tab.add_row("Flat ex time", str(self.flat_time))
        tab.add_row("Execution time", str(self.global_timer))
        tab.add_row("Avg waiting time for execution start", str(self.stats.avg_waiting_time))
        tab.add_row("Avg exec waiting time", str(self.stats.avg_exec_waiting_time))

        return tab
