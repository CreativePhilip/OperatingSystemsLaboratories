from pprint import pprint
from random import seed
from typing import Dict

from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.table import Table


from lab1.schedulers import fsfc_scheduler, Rotational, sjf_non_preemptive, sjf_preemptive
from lab1.simulation import Simulation
from utils.queue import ProcessQueue, ProcessSorting
from copy import deepcopy


seed(1234)


def simulate(data: Dict):
    console = Console()
    queue = ProcessQueue()
    queue.fill_randomly(data["process_count"],
                        data["min_ex_t"],
                        data["max_ex_t"],
                        data["max_toa"])

    console.print(param_table(data))

    if data["verbose"]:
        console.print(queue.table(ProcessSorting.ET))

    s1 = Simulation(deepcopy(queue), fsfc_scheduler, "FSFC Scheduler")
    s2 = Simulation(deepcopy(queue), sjf_non_preemptive, "JSF Non Preemptive Scheduler")
    s3 = Simulation(deepcopy(queue), sjf_preemptive, "JSF Preemptive Scheduler")
    s4 = Simulation(deepcopy(queue), Rotational(), "Rotational Scheduler")

    s1.simulate()
    s2.simulate()
    s3.simulate()
    s4.simulate()

    stats1 = [
        s1.report(),
        s4.report()
    ]

    stats2 = [
        s2.report(),
        s3.report()
    ]

    console.print(Columns([Panel(i, expand=True) for i in stats1]))
    console.print(Columns([Panel(i, expand=True) for i in stats2]))


def param_table(data: Dict):
    tab = Table(title="Process queue generation parameters", style="bold", title_style="bold magenta")

    tab.add_column("key", justify="right", style="cyan")
    tab.add_column("value", justify="left", style="bold green")

    tab.add_row("Process count", str(data["process_count"]))
    tab.add_row("Minimal execution time", str(data["min_ex_t"]))
    tab.add_row("Maximum execution time", str(data["max_ex_t"]))
    tab.add_row("Maximum time of arrival", str(data["max_toa"]))
    tab.add_row("Verbose logging", str(data["verbose"]))

    return tab
