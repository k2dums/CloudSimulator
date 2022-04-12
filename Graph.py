#This class is simply for showing the graph .for comparison,or show relativity with various parameters
import matplotlib.pyplot as plt
class Graph():
    def __init__(self) -> None:
        pass
    def plotBarGraph(names,values):
        plt.bar(names,values,color='blue',width=0.4)
        plt.xlabel=("Algorithms")
        plt.ylabel=("Time Taken")
        plt.title=("Time taken for different Algorithms")
        plt.show()
        