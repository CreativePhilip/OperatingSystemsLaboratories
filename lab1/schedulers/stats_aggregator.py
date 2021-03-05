from statistics import mean


class SchedulerStatistics:
    def __init__(self):
        self.waiting_times = []
        self.exec_waiting_times = []

    def add_waiting(self, dt: int):
        self.waiting_times.append(dt)

    @property
    def avg_exec_waiting_time(self):
        return mean(self.exec_waiting_times)

    @property
    def avg_waiting_time(self):
        return mean(self.waiting_times)
