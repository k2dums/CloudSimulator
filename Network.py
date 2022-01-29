#This class keeps a track of all the layer created 
#The layer object manipulated here
#This class also makes the connection between the the cluster of the a layer and cluster of different layer
from Layer import Layer
import numpy as np
class Network:
    __NETWORK_ID=0
    #The layerid needs to be passed during the creation of a layaer and updated likewise
    def __init__(self) -> None:
        self.__networkId=Network.__NETWORK_ID
        self.__networkLayers=np.array([])
        self.__layerId=0
        Network.__NETWORK_ID+=1
    
    def createLayer(self):
        layer=Layer(self.getLayerId())
        self.__updateLayerId()
        layer.specificationRequest()
        self.__networkLayers=np.append(self.__networkLayers,layer)
    
    def printAllLayerSummary(self):
        print(f"All Layer Summary-Network {self.__networkId}".center(100," "))
        for layer in self.__networkLayers:
            assert isinstance(layer,Layer)
            layer.printLayerSummary()
    
    def printLayerSummary(self,n=0):
        print(f"Layer {n} Summary".center(100," "))
        for i,layer in enumerate(self.__networkLayers):
            if i ==n:
                assert isinstance(layer,Layer)
                layer.printLayerSummary()
    
    def makeLayerConnections(self):
        pass
    
    def getLayerId(self)->int:
        return self.__layerId
    
    def __updateLayerId(self)->None:
        self.__layerId+=1
        
        


    

