#This class keeps a track of all the layer created 
#The layer object manipulated here
#This class also makes the connection between the the cluster of the a layer and cluster of different layer
from NetworkConnection import NetworkConnection
from Layer import Layer
import numpy as np
class Network:
    #Statiac variable to track the network id
    __NETWORK_ID=0
    #The layerid needs to be passed during the creation of a layaer and updated likewise
    def __init__(self) -> None:
        #This sets the network id of the network data structure=[Layer object,Layer object ]
        self.__networkId=Network.__NETWORK_ID
        #This keeps a track of the layers in the network
        self.__networkLayers=np.array([])
        #this keeps a track of the layerid , here it is important to pass it to the Layer object and value is incremented in the Network Class
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
        for i,layer in enumerate(self.__networkLayers):
            if i ==n:
                assert isinstance(layer,Layer)
                layer.printLayerSummary()
    
    def makeLayerConnections(self):
        print(f"\nConnection Specification for the Network {self.__networkId}")
        #This is for the connection between the cluster layer of a layer to the cluster layer of another layer
        self.__connectionMatrix=np.zeros((self.getNumberofLayers,self.getNumberofLayers,1))
        for layerA in range(len(self.__networkLayers)):
            for LayerB in range(layerA+1,len(self.__networkLayers)):
                if layerA==LayerB:
                    continue
                connection=NetworkConnection(layerA,LayerB,self.__networkLayers[layerA,self.__networkLayers[LayerB]])
                self.__connectionMatrix[layerA][LayerB][1]=connection



      



    
    def getLayerId(self)->int:
        return self.__layerId
    
    def __updateLayerId(self)->None:
        self.__layerId+=1

    def getnetworkLayers(self):
        return self.__networkLayers
    def getconnectionMatrix(self):
        return self.__connectionMatrix
    def getNumberofLayers(self):
        return len(self.__networkLayers)
        
network=Network()
network.createLayer()
network.createLayer()
network.makeLayerConnections()
print(network.getconnectionMatrix())

        


    

