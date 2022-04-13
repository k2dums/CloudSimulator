from Network import Network
from Layer import Layer
from DeviceNode import DeviceNode
from Mobile import DeviceNode
from Station import Station
from Cluster import Cluster
from Broker import Broker

class Algorithm:

    FCFS:int=1
    COFFGA:int=2
    CONFGA:int=3

    def __init__(self,network,broker) -> None:
        self.__network=network
        assert isinstance(self.__network,Network)
        self.__broker=broker
        assert isinstance(self.__broker,Broker)
        

        
    
    def resourceAllocation (self,algorithm=1):
        if algorithm == 1:
            self.FCFS()
        elif algorithm == 2:
            self.COFFGA()
        elif algorithm == 3:
            self.CONFGA()


        
        
    def FCFS(self):
        network=self.__network
        assert isinstance(network,Network)  
        broker=self.__broker
        assert isinstance(broker,Broker)
        layers=network.getNetworkLayers()
        for layer in layers:
            assert isinstance(layer,Layer)
            clusters=layer.getClusters()
            for cluster in clusters:
                assert isinstance(cluster,Cluster)
                for device in cluster.getDevices():
                    assert isinstance(device,DeviceNode)
                    broker.assignLinearResources(device)
                    if broker.isResourceEmpty():
                        return 
    
    def COFFGA():
        pass
    def CONFGA():
        pass

    def GA():
        pass
        
    
                    
                    



