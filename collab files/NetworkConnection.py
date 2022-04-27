#This class is reponsible to keep a track of the cluster
#which is connected to another cluster in another layer
#Since a layer can have mulitple clusters ,therefore need to track
#which cluster is connecting to which cluster between two layers
from Cluster import Cluster
from Layer import Layer
import numpy as np
class NetworkConnection:
    def __init__(self,start,end,layerA,layerB)  :
        assert isinstance(layerA,Layer) and isinstance(layerB,Layer)
        self.__layerA=layerA
        self.__layerB=layerB
        self.__connection=np.zeros( ( layerA.getNoClusters(), layerB.getNoClusters() ) )
        self.makeConnection()
   
    #this function makes the connection between clusters of two layers(adjacent)
    def makeConnection(self):
        print(f"\nSetting up connection betweene Layer {self.__layerA.getId()} and Layer {self.__layerB.getId()}")
        print("[y] for Connection else [n]")                  
        # for clusterA in range(self.__layerA_clusters):
        #     for clusterB in range(self.__layerB_clusters):
        #         print(f"Connection between Layer{self.__start}-Cluster {clusterA} and  Layer{self.__end}-Cluster {clusterB}")
        #         userInput="None"
        #         while not(userInput == "y") and not(userInput == "n"):
        #             userInput=input()
        #             if not(userInput=='y') and not(userInput=='n'):
        #                 print("Error give a valid input")
        #         assert userInput=='y' or userInput=='n'
        #         if userInput=='y':
        #             self.__connection[clusterA][clusterB]=1
        #         elif userInput=='n':
        #             self.__connection[clusterA][clusterB]=0
        layerA=self.__layerA
        layerB=self.__layerB
        assert isinstance(layerA,Layer)
        assert isinstance(layerB,Layer)
        for clusterA in layerA.getClusters():
            for clusterB in layerB.getClusters():
                assert isinstance(clusterA,Cluster) and isinstance(clusterB,Cluster)
                print( f"Connection between Layer-{layerA.getId()}-Cluster{clusterA.getId()} and Layer{layerB.getId()}-Cluster {clusterB.getId()}" )
                userInput="None"
                while not(userInput == "y") and not(userInput == "n"):
                    userInput=input()
                    if not(userInput=='y') and not(userInput=='n'):
                        print("Input Error: give a valid input")
                if userInput=='y':
                    self.__connection[clusterA.getId()][clusterB.getId()]=1
                elif userInput=='n':
                    self.__connection[clusterA.getId()][clusterB.getId()]=0
                    

                
                
                
        
    
    #Setters and getters for the NetworkConnection Class
    def getFrom(self) :
        return self.__layerA.getId()

    def getTo(self) :
        return self.__layerB.getId()
    def getNetworkConnection(self):#Returns the connection matrix between two layers 
        return self.__connection