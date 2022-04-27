#This class is simply for showing the graph .for comparison,or show relativity with various parameters
from random import random
import matplotlib.pyplot as plt
import numpy.random as np
class Graph():
    def __init__(self) -> None:
        pass
    #This plots the bar graph for time vs various algorithms in definite setup
    def plotBarGraph(values,names=[]):
        plt.bar(names,values,color='blue',width=0.4)
        plt.xlabel("Algorithms")
        plt.ylabel("Time Taken")
        plt.title("Time taken for different Algorithms")
        plt.show()

    def linearGraph(algoNames,taskSize:list,timeList):

        #timeList=[ [time taken by algo 1],[time taken by algo 2]  ]
        
        if len(algoNames) != len(timeList):
            print("Error:Size of Algorithm mismatached time size")


        for no,name in enumerate(algoNames):
            c=np.rand(3)
            plt.plot(taskSize,timeList[no],color=c,label=f'{name}')
          

        plt.xlabel("No of Tasks")
        plt.ylabel("Time Taken")
        plt.title("Algorithms Time taken Vs Task Size")
        plt.legend(bbox_to_anchor=(1,1.04), loc="upper right",fontsize=7)
        plt.show()

    
    def lineGraph(algoNames,taskSize:list,timeList):
        #timeList=[ [time taken by algo 1],[time taken by algo 2]  ]
        if len(algoNames) != len(timeList):
            print("Error:Size of Algorithm mismatached time size")


        for no,name in enumerate(algoNames):
            c=np.rand(3)
            i=0
            j=0
            flag=False
            while (i<(len(taskSize)-1) and j< ( len(timeList[no]) -1) ):
                p1_x=taskSize[i]
                p2_x=taskSize[i+1]
                p1_y=timeList[no][j]
                p2_y=timeList[no][j+1]
                x=[p1_x,p2_x]
                y=[p1_y,p2_y]
                if not(flag):
                    plt.plot(x,y,color=c,label=f"{name}")
                    flag=True
                else:
                    plt.plot(x,y,color=c)
                i+=1
                j+=1

        plt.xlabel("No of Tasks")
        plt.ylabel("Time Taken")
        plt.title("Algorithms Time taken Vs Task Size")
        plt.legend(bbox_to_anchor=(1,1.04), loc="upper right",fontsize=7)
        plt.show()
       





        