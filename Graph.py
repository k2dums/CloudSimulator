
import matplotlib.pyplot as plt
import numpy.random as np
class Graph():
    """
    This class is simply for showing the graph for comparison,or show relativity with various parameters\n
    """
    def __init__(self) -> None:
        pass
    def plotBarGraph(names=[],values=[],title="Time taken for different Algorithms",xlabel="Algorithms",ylabel="Time Taken (s)"):
        """
        This plots the bar graph for time vs various algorithms in definite setup\n
        """

        plt.bar(names,values,color='blue',width=0.4)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.show()


    def linearGraph(algoNames,taskSize:list,timeList:list[list[int]]):
        """
        Plots the graph in a straight linear way\n
        algoName:list[string] that will be printed as a label\n
        x:list[int] values that will be printed in the  axis\n
        timeList=[ [time taken by algo 1],[time taken by algo 2]  ]\n
        """
        #timeList=[ [time taken by algo 1],[time taken by algo 2]  ]
        
        if len(algoNames) != len(timeList):
            print("Error:Size of Algorithm mismatached time size")


        for no,name in enumerate(algoNames):
            c=np.rand(3)
            plt.plot(taskSize,timeList[no],color=c,label=f'{name}')
          

        plt.xlabel("No of Tasks")
        plt.ylabel("Time Taken (s)")
        plt.title("Algorithms Time taken Vs Task Size")
        plt.legend(bbox_to_anchor=(1,1.04), loc="upper right",fontsize=7)
        plt.show()

    
    def lineGraph(algoNames,taskSize:list,timeList:list[list[int]]):
        """
         Plots the graph \n
         legend_text:list[string] the text that will be printed as label\n
         x:list[int] that values that will be in x axis\n
         timeList=[ [time taken by algo 1],[time taken by algo 2]  ]\n
         timeList=[ [time taken by algo 1],[time taken by algo 2]  ]
        """
       
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
        plt.ylabel("Time Taken (s)")
        plt.title("Algorithms Time taken Vs Task Size")
        plt.legend(bbox_to_anchor=(1,1.04), loc="upper right",fontsize=7)
        plt.show()



        