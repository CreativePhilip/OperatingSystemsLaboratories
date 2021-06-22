from typing import List

from lab5.params import Params


class Process:

    def __init__(self, time: int, weight: float, uuid: int, processor: int):
        self.processor = processor
        self.uuid = uuid
        self.weight = weight
        self.time = time

    def merge(self, data):
        for proc in data:
            if self.processor == proc.uuid:
                proc.add(self)

    def __eq__(self, other):
        if not isinstance(other, Process):
            return False

        return self.time == other.time and self.uuid == other.uuid


class Cpu:
    def __init__(self, uuid: int):
        self.executed: List[Process] = []
        self.waiting: List[Process] = []

        self.uuid = uuid
        self.load = 0
        self.has_just_finished = False

    @property
    def is_overloaded(self):
        return self.load > Params.max

    @property
    def is_idle(self):
        return len(self.executed) == 0 and len(self.waiting) == 0

    @property
    def ready_for_more_processes(self):
        return self.load < Params.min

    @property
    def get_exec_weights(self):
        w = 0
        for proc in self.executed:
            w += proc.weight
        return w

    def remove(self, proc: Process):
        self.load -= proc.weight

        if proc in self.executed:
            self.executed.remove(proc)

        if proc in self.waiting:
            self.waiting.remove(proc)

    def add(self, proc: Process):
        if (self.load + proc.weight) < Params.max:
            self.executed.append(proc)
        else:
            self.waiting.append(proc)

        self.load += proc.weight

    def execute(self):
        self.has_just_finished = False
        for_removal = []

        for proc in self.executed:
            proc.time -= 1
            if proc.time <= 0:
                for_removal.append(proc)

        for dead_proc in for_removal:
            self.executed.remove(dead_proc)
            self.load -= dead_proc.weight

        if len(for_removal) == 0:
            self.has_just_finished = True
            for_removal = []

        for proc in self.waiting:
            if proc.weight + self.get_exec_weights >= Params.max:
                break

            self.executed.append(proc)
            for_removal.append(proc)

        for proc in for_removal:
            if proc in self.waiting:
                self.waiting.remove(proc)

    @staticmethod
    def acquire(cpus: List["Cpu"], uuid: int):
        for cpu in cpus:
            if cpu.uuid == uuid:
                return cpu

    def __eq__(self, other):
        if not isinstance(other, Cpu):
            return False

        return self.uuid == other.uuid
