#This class is simply for showing the graph .for comparison,or show relativity with various parameters
import matplotlib.pyplot as plt
import numpy.random as np
class Graph():
    def __init__(self) -> None:
        pass
    def plotBarGraph(names=[],values=[],title="Time taken for different Algorithms",xlabel="Algorithms",ylabel="Time Taken"):
        """
        This plots the bar graph for time vs various algorithms in definite setup
        """

        plt.bar(names,values,color='blue',width=0.4)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.show()

    def linearGraph(legend_text,x:list,timeList:list[list[int]],title="Algorithms Time taken Vs Task Size",xlabel="No of Tasks",ylabel="Time Taken"):
        """
        Plots the graph in a straight linear way
        algoName:list[string] that will be printed as a label
        x:list[int] values that will be printed in the  axis
        timeList=[ [time taken by algo 1],[time taken by algo 2]  ]
        """
      
        
        if len(legend_text) != len(timeList):
            print("Error:Size of Algorithm mismatached time size")


        for no,name in enumerate(legend_text):
            c=np.rand(3)
            plt.plot(x,timeList[no],color=c,label=f'{name}')
          

        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.legend(bbox_to_anchor=(1,1.04), loc="upper right",fontsize=7)
        plt.show()

    
    def lineGraph(legend_text=[], x:list=[],timeList:list[list[int]]=[],title="Algorithms Time taken Vs Task Size",xlabel="No of Tasks",ylabel="Time Taken"):
        """
        Plots the graph 
        legend_text:list[string] the text that will be printed as label
        x:list[int] that values that will be in x axis
        timeList=[ [time taken by algo 1],[time taken by algo 2]  ]
        """
      
        if len(legend_text) != len(timeList):
            print("Error:Size of Algorithm mismatached time size")


        for no,name in enumerate(legend_text):
            c=np.rand(3)
            i=0
            j=0
            flag=False
            while (i<(len(x)-1) and j< ( len(timeList[no]) -1) ):
                p1_x=x[i]
                p2_x=x[i+1]
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

        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.legend(bbox_to_anchor=(1,1.04), loc="upper right",fontsize=7)
        plt.show()
       





        