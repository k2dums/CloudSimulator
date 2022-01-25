import numpy as np
import pandas as pd
import random
import math
import operator
import pickle #we have to use pickle
import matplotlib.pyplot as plt
import os
import copy

#numpy has it owns abs and sqrt function and will be changing it from the math.sqrt and math.abs

def initalSolution(n_trucks,path_truck):
    # print('path per truck',path_truck)
    # print('no of trucks',n_trucks)
    sol=[]
    count=0
   
    for i in range(int(n_trucks)):
        listb=[]
        for j in range(int(path_truck)):
            listb.append(count)
            count=count+1
        sol.append(listb)
    # print(sol)
    
    for i in range(100):
        x1=random.randint(0,n_trucks-1)
        x2=random.randint(0,n_trucks-1)
        y1=random.randint(0,path_truck-1)
        y2=random.randint(0,path_truck-1)
        swapOperator(sol, x1, y1, x2, y2)
    return sol



# def impr_initalSolution(n_trucks,file_pt):
#     #Here we use the concept of k means clustering
#     #we need to mention the cluster size = path_truck
#     k=n_trucks
#     positions=np.empty
#     for i in range(len(file_pt)):
#         positions.append( [ file_pt.iloc[i,1],file_pt.iloc[i,2] ] )
        
#     X=positions
#     plt.scatter(X)
#     #Lets write clustering algorithm
#     # midpoints=set()
#     # while len(midpoints)<k:
#     #     random_no=random.randint(0, len(positions()))
#     #     midpoints.add(random_no)
    
    
#     # for pos in positions:
#     #     #finding the distandce between midpoints and the points
#     #     distance=np.empty
#     #     for midpoint in midpoints:
#     #         x1=pos[0]
#     #         y1=pos[1]
#     #         x2=positions[midpoint][0]
#     #         y2=positions[midpoint][1]
#     #         distance.append(calcualte_distance(x1,y1,x2,y2))
        
#     kmeans=KMeans(n_clsuters=k,random_state=0).fit(X)
    
#     kmeans.predict()

def plot_graph(sol,df,colors):
    plt.text(0,0,"Depot",horizontalalignment='center',verticalalignment='center')
    counter=0
    for truck,c in zip(sol,colors):
        #plot depot to the truck first position
        p1_x=0
        p1_y=0
        p2_x=df.iloc[truck[0]][1]
        p2_y=df.iloc[truck[0]][2]
        plt.plot([p1_x,p2_x],[p1_y,p2_y],color=c,label=f"truck {counter}")

        for i in range(len(truck)-1):
            p1=truck[i]
            p2=truck[i+1]
            plt.plot( [df.iloc[p1][1],df.iloc[p2][1]],[df.iloc[p1][2],df.iloc[p2][2]],color=c,)
            
        #from last postion to the depot
        p2_x=0
        p2_y=0
        p1_x=df.iloc[ truck[-1]][1]
        p1_y=df.iloc[ truck[-1]][2]
        plt.plot([p1_x,p2_x],[p1_y,p2_y],color=c,)
        
        #plotting the points with customer number
        for location in truck:
            x=df.iloc[location][1]
            y=df.iloc[location][2]
            plt.plot(x,y,'o',color=c)
            plt.text(x+0.02,y,location,horizontalalignment='left',verticalalignment='center')
        counter+=1
        # plt.legend(loc='upper right',fontsize=7,)
        plt.legend(bbox_to_anchor=(1.04,1), loc="upper left")
    plt.show()
        

def plot_cost_X_iterations(cost_list):
    n=len(cost_list)
    print()
    plt.xlabel("Iterations")
    plt.ylabel("Cost")
    plt.plot( list(range(n)),cost_list,'-r')
    plt.show()
    
       
    
 
        
        
        
        
        
    
    
def calcualte_distance(x1,y1,x2,y2):
    return np.sqrt( (x1-x2)**2+(y1-y2)**2)
      

        
    






def sorter(file_pt):
     customer_dist=dict()
     for i in range(len(file_pt)):
         customer_dist[i]=((file_pt.iloc[i,1]) ** 2 + (file_pt.iloc[i,2] ) ** 2) ** 0.5
     sorted_d = dict(sorted(customer_dist.items(), key=operator.itemgetter(1),reverse=True))
     return sorted_d
 
    
 
def hillclimbingalgo(n,sol,n_trucks,path_truck,dist,file_pt):
    iterations=int(input('Give the number of iterations = '))
    # iterations=1000
    cost_list=[]
    for i in range(iterations):
        current_cost=cost(sol,dist,file_pt)[0]
        cost_list.append(current_cost)
        x1=random.randint(0,n_trucks-1)
        x2=random.randint(0,n_trucks-1)
        # y1=random.randint(0,path_truck-1)
        # y2=random.randint(0,path_truck-1)
        y1=random.randint(0,len(sol[x1])-1)
        y2=random.randint(0,len(sol[x2])-1)
        
        check_First_Constraint(sol)
        check_Second_Constraint(sol)
        
        swapOperator(sol, x1, y1, x2, y2)
        if cost(sol,dist,file_pt)[0]>=current_cost:
            #Because the swapped cost is greater ,we revert back
            swapOperator(sol, x1, y1, x2, y2)
            
    result=cost(sol,dist,file_pt)
    delta_value= abs(result[1]-result[2]) 
    # cost_pertruck(sol, dist, file_pt)
    ans=result[0]+delta_value
    # print("total vaue = ",result[0])
    # print("delta value =",delta_value)
    # print("Answer =",ans)
    feas=check_First_Constraint(sol)+check_Second_Constraint(sol)
    return sol,ans,feas,cost_list
        

def swapOperator(sol, x1, y1, x2, y2):
    temp = sol[x1][y1]
    sol[x1][y1] = sol[x2][y2]
    sol[x2][y2] = temp



    
def cost(sol,dist,file_pt):
    #Calculating the Distance travelled by each truck driver
    total_value=0
    min_dist=-1
    max_dist=-1
    
    for drivers in sol:
        cost_truck=0
        #calculating from depot to the first location
        x=file_pt.iloc[drivers[0],1]
        y=file_pt.iloc[drivers[0],2]
        distance=math.sqrt(x**2 + y**2)
        cost_truck=cost_truck+distance
        
        #Calculating inbw destinations
        for i in range(len(drivers)-1):
            
            distance=dist[drivers[i]][drivers[i+1]]   
            cost_truck=cost_truck+distance

        #calcluating last postion to depot
        x=file_pt.iloc[drivers[-1],1]
        y=file_pt.iloc[drivers[-1],2]
        distance=math.sqrt(x**2 + y**2)
        cost_truck=cost_truck+distance
        total_value=total_value + cost_truck
        
    
        if max_dist==-1 and min_dist==-1:
            max_dist=cost_truck
            min_dist=cost_truck
                    
        elif cost_truck>max_dist:
            max_dist=cost_truck
                
        elif cost_truck<min_dist:
            min_dist=cost_truck
               
    lister=(total_value,max_dist,min_dist)
    return lister
        
        
        
#if the first truck's first customer is even we return 0,else 1
def check_First_Constraint(sol):
    first_truck=sol[0]
    if first_truck[0]%2==1:
        return 1
    return 0

    
   
    
#if the last truck's last customer is odd we return 0 ,else 1
def check_Second_Constraint(sol):
    last_truck=sol[-1]
    if last_truck[-1]%2==0:
        return 1
    return 0
   
       
        
        
#This function is simply used for debugging
def cost_pertruck(sol,dist,file_pt):
    #Calculating the Distance travelled by each truck driver
    for drivers in sol:
        print("the path taken for the driver =",drivers)
        cost_truck=0
        #calculating from depot to the first location
        x=file_pt.iloc[drivers[0],1]
        y=file_pt.iloc[drivers[0],2]
        distance=math.sqrt(x**2 + y**2)
        print("The distance from first to depot",distance)
        cost_truck=cost_truck+distance
        
        #Calculating in-bw destinations
        for i in range(len(drivers)-1):
            
            distance=dist[drivers[i]][drivers[i+1]]   
            print(f"the distance bw {drivers[i]} and {drivers[i+1]}= ",distance)
            cost_truck=cost_truck+distance
            print("summing the value of cost=",cost_truck)
        
        #calcluating last postion to depot
        x=file_pt.iloc[drivers[-1],1]
        y=file_pt.iloc[drivers[-1],2]
        distance=math.sqrt(x**2 + y**2)
        print("The distance from last to depot",distance)
        cost_truck=cost_truck+distance
        print(cost_truck)
        print("\n\n")
    
            
        
        
        
        

#def genetic_algo():
#We can use genetic algorithm to solve this problem
#Here we assign the list of chromosomes corresponding to the truck and their paths
#these chromosomes are then cross-overed and mutated
#after this we can use selection method to get the best muatated chromosomes between the population  of parent and offspring
#iterate the above process for more generation ,to get the best muatated chromosome 




# file='I2.csv'
Check=False
while(not(Check)):
    file = str(input("Enter .csv file? : "))
    if not ".csv" in file:
        file += ".csv"
    Check=os.path.exists(file)
    if Check==True:
        df = pd.read_csv(file)
    else:
          print("Give a valid file")
         

file_pt=pd.read_csv(file)
n=len(file_pt)
n_trucks=int(n/np.sqrt(n))
path_truck=int(n/n_trucks)
#calculating the distance_matrix between points
dist=np.zeros((n,n))
for i in range(n):
    for j in range(n):
        x1=file_pt.iloc[i,1]
        y1=file_pt.iloc[i,2]
        x2=file_pt.iloc[j,1]
        y2=file_pt.iloc[j,2]
        dist[i][j]=calcualte_distance(x1, y1, x2, y2)

initial_sol=initalSolution(n_trucks,path_truck)
sol=copy.deepcopy(initial_sol)
sol,ans,feas,cost_list=hillclimbingalgo(n,sol,n_trucks,path_truck,dist,file_pt)
colors=[np.random.rand(4) for i in range(len(sol))]
plot_graph(sol,file_pt,colors)
plot_cost_X_iterations(cost_list)

lister=cost(initial_sol, dist, file_pt)
delta_initial=np.abs(lister[1]-lister[2])
tv_intital=lister[0]
initial_ans=tv_intital+delta_initial
initial_feas=check_First_Constraint(initial_sol)+check_Second_Constraint(initial_sol)

print('no of customers',n)
print("no of trucks",n_trucks)
print("My intital solution = \n",initial_sol,end="\n\n")
print("This is my solution path =\n",sol,end="\n\n")
print("The total cost of the solution=",ans)
print("The feasibility of the solution=",feas) 

with open('sol.csv', 'w') as writeFile:
    writeFile.write('\n'.join(str(s) for s in sol))
    writeFile.write('\n')
    writeFile.write(str(ans))
    writeFile.write('\n')
    writeFile.write(str(feas))
    
with open('n.pkl',"wb") as npick:
    pickle.dump(feas,npick)
    pickle.dump(ans,npick)
    pickle.dump(sol,npick)
    pickle.dump(initial_feas,npick)
    pickle.dump(initial_ans,npick)
    pickle.dump(initial_sol,npick)
    

    
with open('n.pkl',"rb") as npick:
    feas1=pickle.load(npick)
    ans1=pickle.load(npick)
    sol1=pickle.load(npick)
    feas2=pickle.load(npick)
    ans2=pickle.load(npick)
    sol2=pickle.load(npick)
    


