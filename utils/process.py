from copy import copy
from random import randint


class Process:
    """
    Process class that represents a process to be executed
    """
    def __init__(self, name, time_of_arrival, execution_time):
        self.name = name
        self.time_of_arrival = time_of_arrival
        self.execution_time = execution_time
        self.execution_time_left = copy(execution_time)
        self.start_time = 0
        self.execution_waiting_time = 0

    def tick(self, global_timer):
        if not self.can_execute(global_timer):
            raise ProcessNotScheduledException()

        if self.execution_time == self.execution_time_left:
            self.start_time = global_timer

        self.execution_time_left -= 1

        if self.execution_time_left == 0:
            self.execution_waiting_time = global_timer - self.start_time - self.execution_time + 1

    def is_finished(self):
        return self.execution_time_left == 0

    def can_execute(self, current_time: int):
        return current_time >= self.time_of_arrival

    @classmethod
    def create_random(cls, name_idx, *, min_execution_time, max_execution_time, max_time_of_arrival) -> "Process":
        return cls(
            name=f"Process: {name_idx}",
            time_of_arrival=randint(0, max_time_of_arrival),
            execution_time=randint(min_execution_time, max_execution_time))

    def __eq__(self, other):
        return other.name == self.name

    def __str__(self):
        return f"{self.name}(toa: {self.time_of_arrival}, et: {self.execution_time}, etl: {self.execution_time_left})"

    def __repr__(self):
        return self.__str__()


class ProcessNotScheduledException(BaseException):
    pass
