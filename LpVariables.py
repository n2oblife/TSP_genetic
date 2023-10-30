# Import PuLP library
from pulp import *

# penser à faire un loader du fichier excel

def LPSolver(nomDuPb:str,boolMaximize:bool, distance:list, distanceCost:float, capacity:list,fixedCost:list = None,demand:list = None):
    ''' The LPSolver solves an optimization problem with the pulp library which needs to be imported beforhand. 
    nomDuPb :       name of the problem to be created , 
    boolMaximize :  True if it aims the objective function is to be the max, False if it aims to be the min,
    distance :      matrix of the distance between the factories and the markets,
    distanceCost :  the cost of 1 unit of distance,
    fixedCost :     the fixed cost of production for a good,
    capacity :      the capcity a factory can produce of one good'''

    if __name__ == "__main__":
        
        #create the decision variables
        n, m = len(distance), len(distance[0])
        v = [ [LpVariable("x{}_{}".format(i+1,j+1), lowBound = 0, cat ='Integer') for j in range(m) ] for i in range(n)]
        
        # create the problem to contain the data depending on the will to maximize or minimize
        if boolMaximize:
            monPb = LpProblem(nomDuPb, LpMaximize)
        else:
            monPb = LpProblem(nomDuPb, LpMinimize)
        
        #adding the objective function
        monPb += distanceCost*sum( (( v[i][j]*distance[i][j] for j in range(m)) for i in range(n)) )

        #adding the constraints
        for i in range(n):
            monPb += sum(v[i]) <= capacity[i]

        for j in range(m):
            monPb += sum([v[i][j] for i in range(n)]) >= demand[j]

        #solution of the problem
        monPb.solve()
        print("Status:", LpStatus[monPb.status]) 

        for x in monPb.variables():
            print(x.name, ' = ', x.varValue)
        print ("Objective value ",nomDuPb," = ", value(monPb.objective))