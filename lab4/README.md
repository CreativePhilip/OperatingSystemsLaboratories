# Lab4
## Abstract
The task of this lab was to prepare a comparison between various Frame allocation algorithms.
1. RANDOM -> Randomly choose frames
2. PROPORTIONAL -> Choose frames proportionally to the usage
3. PAGE FAULT FREQUENCY -> Choose frames based on the page fault frequency



## Experimental data
This time there are 3 user adjustable variables
1. PROCESS_AMOUNT -> Number of processes in the simulation 
2. FRAME_AMOUNT -> Number of frames available to the whole system
3. MAX_FRAMES_PER_PROCESS ->  Max number of pages that a process can require

The order of replacement requests was generated randomly, for repeatability before the test the random number generator was seeded with the value 1234567890.

## Results
|          --         	| Page Fault Percentage 	|
|:-------------------:	|:---------------------:	|
|  Proportional faults	|           82          	|
|      Random       	|           60          	|
| Priority faults   	|           55          	|
