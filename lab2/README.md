# Lab 2 Task
## Abstract
The task is to implement the following drive data querying algorithms and compare the avg wait time
for the read requests. <br/>

## Implemented algorithms
1. FIFO simple queue
2. SSTF queue sorted by the seek time
3. Scan sstf, but we go only one way until the end of the range, after which the direction is changed
4. CScan similarly as Scan but after reaching the end we move the RW head to the 0 position
5. EDF queue sorted by the deadline
   
## Backend system 
To ensure results consistent across algorithms a robust backend was required. To achieve that I have created
a Simulation class responsible for the main execution "loop" as well as statistical data collection.
An algorithm was just a plugin into the class. Again to ensure consistency I have created a type that
the functions performing process selecting had to conform to.
```python
ALGO_LAMBDA: Type = Callable[[RequestQueue, ReadRequest, int], Tuple[Optional[ReadRequest], int]]


def algorithm(q: RequestQueue, previous_request: ReadRequest, read_head: int) -> Tuple[
        Optional[ReadRequest], int]:
```

### Queue creation
To avoid the need for calculating a chance for a new request every "tick" and for keeping count of the globally created
request and to ensure consistent request creation across other algorithms. The queue is pre-allocated before starting
the simulation. In addition to a unique name and data location property each process had a time_of_arrival value
which indicated after which tick number can the process be considered for execution.  

#### The creation of the global queue is parametrized with 4 values:
1. Number of requests to create
2. Max time of arrival
3. Max deadline
4. Data location range

## Generic view of the algorithm function
Every "tick" of the execution loop the selected algorithm had 3 options:
1. To leave the current request for another "round" of execution
2. To swap the current request for a different one
3. To return None, which means that currently there are no processes in the queue
4. To select the new position of the RW head

## Results
|   -   | AVG SEEK TIME (ticks) | TOTAL SIM TIME (ticks) |
|:-----:|:---------------------:|:----------------------:|
|  FIFO |         79.31         |          10122         |
|  SSTF |         50.855        |          10077         |
|  SCAN |         52.56         |          10077         |
| CSCAN |         60.675        |          10052         |
|  EDF  |         84.445        |          10081         |


