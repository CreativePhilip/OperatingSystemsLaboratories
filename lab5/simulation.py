import random
from copy import copy, deepcopy
from statistics import mean
from typing import List, Optional

from lab5.params import Params
from lab5.process import Cpu, Process


class Simulation:

    @staticmethod
    def gen_data():
        cpus: list[Cpu] = []
        processes: list[Optional[Process]] = []

        for i in range(Params.size):
            cpus.append(Cpu(i))

        for i in range(Params.processes):
            random_value = random.random()

            if random_value < 0.2:
                processes.append(None)
                continue

            rand_time = random.randint(0, Params.max_time)
            rand_weight = random.random() * Params.max_weight
            rand_proc = random.randint(0, Params.size)

            processes.append(Process(rand_time, rand_weight, i, rand_proc))

        return cpus, processes

    @staticmethod
    def find_receiver(cpus: List[Cpu], sender: Cpu, proc: Process):
        to_query = deepcopy(cpus)
        to_query.remove(sender)

        requests = 0
        while len(to_query) != 0:
            requests += 1

            idx = random.randint(0, len(to_query) - 1)
            current = to_query[idx]
            to_query.remove(current)

            if current.load + proc.weight < Params.max:
                return requests, sender

    @staticmethod
    def migrate(sender: Cpu, receiver: Cpu, proc: Process):
        sender.remove(proc)
        receiver.add(proc)

    @staticmethod
    def add_loads(data: List[Cpu], loads: List[float]):
        for cpu in data:
            load = cpu.load
            loads.append(load)

    @staticmethod
    def execute(cpus: List[Cpu]):
        for cpu in cpus:
            cpu.execute()

    @staticmethod
    def is_finished(cpus: List[Cpu]):
        for cpu in cpus:
            if not cpu.is_idle:
                return False
        return True

    @staticmethod
    def migration_minmax(cpus: List[Cpu], request: int, migrations: int):
        for cpu in cpus:
            if cpu.has_just_finished and cpu.ready_for_more_processes:
                l_requests, l_proc = Simulation.find_sender(cpus, cpu)
                request += l_requests
                if l_proc.uuid != cpu.uuid:
                    Simulation.migrate(l_proc, cpu, l_proc.waiting[0])
                    migrations += 1

        return request, migrations

    @staticmethod
    def random(cpus: List[Cpu], processes: List[Process]):
        migrations = 0
        requests = 0
        loads = []

        for proc in processes:
            if proc is not None:
                proc.merge(cpus)
                current = Cpu.acquire(cpus, proc.processor)

                if current is None:
                    continue

                if current.is_overloaded:
                    f_req, f_proc = Simulation.find_receiver(cpus, current, proc)
                    requests += f_req
                    if current.uuid == f_proc.uuid:
                        Simulation.migrate(current, f_proc, proc)
                        migrations += 1

            Simulation.add_loads(cpus, loads)
            Simulation.execute(cpus)

        while not Simulation.is_finished(cpus):
            Simulation.add_loads(cpus, loads)
            Simulation.execute(cpus)

        avg_load = mean(loads)
        var = variation(loads, avg_load)

        print("Rand algo")
        print(f"load variation: {var}")
        print(f"avg load: {avg_load}")
        print(f"request amount: {requests}")
        print(f"migrations count: {migrations}")

    @staticmethod
    def minmax(cpus: List[Cpu], processes: List[Process]):
        migrations = 0
        requests = 0
        loads = []

        for proc in processes:
            if proc is not None:
                proc.merge(cpus)

            l_req, l_mig = Simulation.migration_minmax(cpus, requests, migrations)
            requests = l_req
            migrations = l_mig

            Simulation.add_loads(cpus, loads)
            Simulation.execute(cpus)

        while not Simulation.is_finished(cpus):
            l_req, l_mig = Simulation.migration_minmax(cpus, requests, migrations)
            requests = l_req
            migrations = l_mig

            Simulation.add_loads(cpus, loads)
            Simulation.execute(cpus)

        avg_load = mean(loads)
        var = variation(loads, avg_load)

        print("minmax algo")
        print(f"load variation: {var}")
        print(f"avg load: {avg_load}")
        print(f"request amount: {requests}")
        print(f"migrations count: {migrations}")

    @staticmethod
    def find_sender(cpus: List[Cpu], cpu: Cpu):
        to_query = deepcopy(cpus)
        to_query.remove(cpu)
        requests = 0

        while len(to_query) != 0:
            requests += 1
            idx = random.randint(0, len(to_query) - 1)
            current = to_query[idx]
            to_query.remove(current)

            if current.is_overloaded:
                return requests, current
        return requests, cpu


def variation(loads: List[float], avg: float):
    sum_ = 0
    for load in loads:
        sum_ += (load - avg) ** 2
    return sum_ / len(loads)


if __name__ == '__main__':
    d1, d2 = Simulation.gen_data()
    Simulation.random(deepcopy(d1), deepcopy(d2))
    print()
    Simulation.minmax(deepcopy(d1), deepcopy(d2))
