#This class is for allocating the resources and also is reponsible for the schdeduling algorithm used
#It assigns the broker id to the device when allocating the resources to it
#Concept of multithreading can be used to simulate,and say one sec processing makes simulation runs for 1 ms
from Network import Network
from DeviceNode import DeviceNode
from Mobile import Mobile
from Station import Station
from Layer import Layer
class Broker:
    __BROKER_ID=0
    def __init__(self,network) -> None:
        self.__network=network
        self.__brokerId=Broker.__BROKER_ID
        self.__deviceId=0
        Broker.__BROKER_ID+=1
    
    def __init__(self,network,resourceList:list) -> None:
        self.__network=network
        self.__brokerId=Broker.__BROKER_ID
        self.__deviceId=0
        self.__resourceList=resourceList
        Broker.__BROKER_ID+=1

    #A broker is responsible for a layer only
    # def __init__(self,network,resourceList:list,layerno) -> None:
    #     self.__network=network
    #     self.__brokerId=Broker.__BROKER_ID
    #     self.__deviceId=0
    #     self.__resourceList=resourceList
    #     Broker.__BROKER_ID+=1
        
        
    
    def setResourceList(self,resourceList)->list:
        self.__resourceList=resourceList
    
    def __getBrokerDeviceId(self)->str:
        temp=f"#{self.__brokerId}_{self.__deviceId}"
        self.__deviceId+=1
        return temp
    
    def getAllDeviceState():
        pass
    def getActiveDeviceState():
        pass
    def printActiveDeviceSummary():
        pass
    def printAllDeviceSumamry():
        pass
    def allocateResource():
        pass
    def allocateResource(algorithm):
        pass
    def startSimulation():
        pass
    def deviceBreakDown(deviceObj):
        pass
    def updateDeviceStatus(deviceObj):
        pass
    def simualationSummary():
        pass