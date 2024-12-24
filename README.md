# Travelling-Salesman-Problem-simulated_annealing-

Simulated annealing belongs to a group of algorithms that use local improvement to search for solutions in the space of possible states. At the same time, the algorithm attempts to avoid getting stuck in a local extremum. Starting from the current node, the algorithm generates successors in a standard manner and selects one. If the chosen successor has a better evaluation, it transitions to it with 100% certainty. If the successor has a worse evaluation, the transition may still occur, but only with a probability less than 100%. If the successor is rejected, another one is tested. If no transition is possible to any successor, the algorithm terminates, and the current node is considered the solution. To find the global extremum, a proper schedule for adjusting the probability of selecting a worse successor is critical. Initially, the probability is relatively high and gradually decreases to zero.

An important parameter of this algorithm is the schedule for adjusting the probability of selecting a worse successor. A schedule that is too short (fast) may cause the algorithm to fail to bypass local extrema, while an overly long schedule will extend the runtime, as it will circle around the optimal solution.

Program Operation:
The algorithm runs 10 times on randomly generated cities and calculates the average shortest distance and its corresponding path. 

Notation:
Best Path: [18, 8, 11, 3, 12, 0, 14, 15, 16, 19, 1, 7, 13, 10, 17, 5, 2, 6, 9, 4]
-Number of points along which the algorithm traversed.

City 18: (105, 162) 
- x and y coordinates of the city within a 200x200 grid.
