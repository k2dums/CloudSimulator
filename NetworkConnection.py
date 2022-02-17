#This class is reponsible to keep a track of the cluster
#which is connected to another cluster in another layer
#Since a layer can have mulitple clusters ,therefore need to track
#which cluster is connecting to which cluster between two layers
from Layer import Layer
import numpy as np
class NetworkConnection:
    def __init__(self,start,end,layerA_obj,layerB_obj) -> None:
        self.__start=start
        self.__end=end
        assert isinstance(layerA_obj,Layer) and isinstance(layerB_obj,Layer)
        self.__layerA_obj=layerA_obj
        self.__layerB_obj=layerB_obj
        self.__layerA_clusters=layerA_obj.getCluster()
        self.__layerB_clusters=layerB_obj.getCluster()
        self.__connection=np.zeros((self.__layerA_clusters,self.__layerB_clusters))
        self.makeConnection()
   
    #this function makes the connection between clusters of two layers(adjacent)
    def makeConnection(self):
        print(f"\nSetting up connection betweene Layer {self.__start} and Layer {self.__end}")
        print("[y] for Connection else [n]")                  
        for clusterA in range(self.__layerA_clusters):
            for clusterB in range(self.__layerB_clusters):
                print(f"Connection between Layer{self.__start}-Cluster {clusterA} and  Layer{self.__end}-Cluster {clusterB}")
                userInput="None"
                while not(userInput == "y") and not(userInput == "n"):
                    userInput=input()
                    if not(userInput=='y') and not(userInput=='n'):
                        print("Error give a valid input")
                assert userInput=='y' or userInput=='n'
                if userInput=='y':
                    self.__connection[clusterA][clusterB]=1
                elif userInput=='n':
                    self.__connection[clusterA][clusterB]=0
                
                
                
        
    
    #Setters and getters for the NetworkConnection Class
    def getFrom(self)->None:#Gets the id  of starting  layer
        return self.__start
    def getTo(self)->None:#Gets the id of  next layer
        return self.__end
    def getNetworkConnection(self):#Returns the connection matrix between two layers 
        return self.__connection