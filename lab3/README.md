# Lab3 
## Abstract
The task of this lab was to prepare a comparison between various memory page replacement algorithms.
1. FIFO -> Quite simple, a fifo queue of pages in memory
2. RAND -> Quit simple as well, in case of a page fault pick at random a page to swap
3. LRU -> This is a little more sophisticated algorithm, it requires for us to hold a count of long ago each page was used. On the basis of this data we pick the least used page for replacement.
4. OPT -> Optimal algorithm, if our scheduler were to be omnipotent it could look into the future and check which page from the cache is going to be used the least and replace that one. This is the algorithm that has the least page faults, and is used as a benchmark target.


## Experimental data
This time there are 3 user adjustable variables
1. MAX_PAGE_NUMBER -> The number of discrete pages, it is important to remember that for any meaningful data this number has to be greater that the param no. 3. Otherwise, every algorithm will have 0% page faults.
2. REQUEST_AMOUNT -> The amount of requests to check, you can think of it as the length of the test. This value should be an order of magnitude greater that the param no.1 . 
3. MEM_CACHE_AMOUNT -> How many pages are we caching in the memory.

The order of replacement requests was generated randomly, for repeatability before the test the random number generator was seeded with the value 420.

## Results
|          --         	| Page Fault Percentage 	|
|:-------------------:	|:---------------------:	|
|  First In First Out 	|           74          	|
|        Random       	|           75          	|
| Least Recently Used 	|           67          	|
|       Optimal       	|           55          	|
