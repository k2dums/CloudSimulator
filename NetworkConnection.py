from Layer import Layer
import numpy as np
class NetworkConnection:
    def __init__(self,start,end,layerA_obj,layerB_obj) -> None:
        self.__start=start
        self.__end=end
        self.__layerA_obj=layerA_obj
        self.__layerB_obj=layerB_obj
        self.__layerA_clusters=layerA_obj.getClusters()
        self.__layerB_clusters=layerB_obj.getClusters()
        self.__connection=np.zeros(self.__layerA_clusters,self.__layerB_clusters)
        self.makeConnection()
   
    def makeConnection(self):
        print("Setting up connection betweene Layer {self.__start} and Layer {self.__end}")
        print("[y] for Connection else [n]")                  
        for clusterA in range(self.__layerA_clusters):
            for clusterB in range(self.__layerB_clusters):
                print(f"Connection between Cluster {clusterA} and Cluster {clusterB}")
                userInput="None"
                while not(userInput == "y") and not(userInput == "n"):
                    userInput=input(f"Connection [y] for connection else [n]:\n")
                    if not(userInput=='y') and not(userInput=='n'):
                        print("Error give a valid input")
                assert userInput=='y' or userInput=='n'
                if userInput=='y':
                    self.__connection[clusterA][clusterB]=1
                elif userInput=='n':
                    self.__connection[clusterA][clusterB]=1
                
                
                
        
    
    
    def getFrom(self)->None:
        return self.__start
    def getTo(self)->None:
        return self.__end