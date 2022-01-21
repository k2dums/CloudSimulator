# -*- coding: utf-8 -*-
"""
Here is example code for approximately solving the TSP using a hill climbing method.
How you might modify this code to produce better results?
@author: Ahmed Kheiri
"""
import pandas as pd
import numpy as np

# Generate a random permutation of the numbers 0 to n-1
def InitialSolution(n):
    sol = list(range(n))
    np.random.shuffle(sol)
    return sol

# This function takes a candidate solution (permutation of the cities) and computes its total distance.
def TotalDistance(sol, dist, n):
    totalDist = 0
    for i in range(n - 1):
        totalDist = totalDist + dist[sol[i]][sol[i+1]]
    # Don't forget to consider the journey from the last city to the first one
    totalDist = totalDist + dist[sol[-1]][sol[0]]
    return totalDist

# Hill climbing algorithm run for 100,000 iterations
def HillClimbing(sol, dist, n):
    # First evaluate the initial solution (its total distance is likely to be high at first)
    solDist = TotalDistance(sol, dist, n)
    # Now carry out the main loop of the algorithm
    for i in range(10000):
        x = np.random.randint(0, n)
        y = np.random.randint(0, n)
        # apply swap operator that swaps two cities and then re-evaluate
        SwapOperator(sol, x, y)
        solDist_new = TotalDistance(sol, dist, n)
        # If the change decreases or maintains the total distance then accept the move; otherwise reject the move
        if solDist_new <= solDist:
            solDist = solDist_new
        else:
            SwapOperator(sol, x, y)

def SwapOperator(sol, s1, s2):
    temp = sol[s1]
    sol[s1] = sol[s2]
    sol[s2] = temp

# The data in the input file is assumed to be in the correct format.
# df_tsp is a constructed dataframe that holds the n coordinates
df_tsp = pd.read_csv('I1.csv')
n = len(df_tsp)

# Here we create a dist list containing n lists, each of n items, all set to 0 initially. dist holds the distances between each pair of locations
# Is the data structure List is the best to represent dist? Think carefully!
dist = [[0 for x in range(n)] for y in range(n)] 
# Now we work out the Euclidean distance between each pair of cities and put this into the dist list
for i in range(n):
    for j in range(n):
        dist[i][j] = ((df_tsp.iloc[i,1] - df_tsp.iloc[j,1]) ** 2 + (df_tsp.iloc[i,2] - df_tsp.iloc[j,2]) ** 2) ** 0.5

# Is the data structure List is the best to represent sol? Think carefully!
# We are now ready to try and solve the problem. First, produce a random starting solution
sol = InitialSolution(n)

# Now carry out the hill climbing procedure
HillClimbing(sol, dist, n)

print(sol)
print(TotalDistance(sol, dist, n))

with open('sol.csv', 'w') as writeFile:
    writeFile.write(','.join(str(s) for s in sol))
    writeFile.write('\n')
    writeFile.write(str(TotalDistance(sol, dist, n)))

print("Run Completed Successfully")