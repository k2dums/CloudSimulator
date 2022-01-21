import random
import pickle

def M(n):
    return n*(n*n+1)/2

def InitialSolution(n):
    sol = []
    for i in range(n):
        sol.append(list(range(i*n + 1,i*n+n + 1)))
    return sol

def Cost(sol):
    obj = 0
    n = len(sol)
    
    for i in range(n):
        sumR = 0
        for j in range(n):
            sumR += sol[i][j]
        obj += abs(M(n) - sumR)
    
    for i in range(n):
        sumC = 0
        for j in range(n):
            sumC += sol[j][i]
        obj += abs(M(n) - sumC)
    
    sumD = 0
    for i in range(n):
        sumD += sol[i][i]
    obj += abs(M(n) - sumD)
    
    sumD = 0
    for i in range(n):
        sumD += sol[i][n-1-i]
    obj += abs(M(n) - sumD)
    return obj

def HillClimbing(sol):
    solCost = Cost(sol)
    for i in range(10000):
        x1 = random.randint(0, len(sol)-1)
        y1 = random.randint(0, len(sol)-1)
        x2 = random.randint(0, len(sol)-1)
        y2 = random.randint(0, len(sol)-1)
        SwapOperator(sol, x1, y1, x2, y2)
        solCost_new = Cost(sol)
        if solCost_new <= solCost:
            solCost = solCost_new
        else:
            SwapOperator(sol, x1, y1, x2, y2)

def SwapOperator(sol, x1, y1, x2, y2):
    temp = sol[x1][y1]
    sol[x1][y1] = sol[x2][y2]
    sol[x2][y2] = temp

n = 3
sol = InitialSolution(n)
HillClimbing(sol)

print(sol)
print(Cost(sol))

print("Run Completed Successfully")

try :
    file = open("record.ms","rb")
    prev_run = pickle.load(file)
    print("Previous solution", prev_run)
    file.close()
except FileNotFoundError :
    print("A new file is created")

file = open("record.ms","wb")
pickle.dump(sol,file)
file.close()
