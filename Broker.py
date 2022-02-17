#This class is for allocating the resources and also is reponsible for the schdeduling algorithm used
#It assigns the broker id to the device when allocating the resources to it
#Concept of multithreading can be used to simulate,and say one sec processing makes simulation runs for 1 ms
from psutil import swap_memory
from sympy import N
from Network import Network
from DeviceNode import DeviceNode
from Mobile import Mobile
from Station import Station
from Layer import Layer


class Broker:
    __BROKER_ID=0
    __state=["CREATED","READY","QUEUED","SUCCESS","FAILED","PAUSED","RESUMED","FAILED_RESOURCE_UNAVAILABLE"]
    
    def __init__(self,network) -> None:
        self.__network=network
        self.__brokerId=Broker.__BROKER_ID
        self.__deviceId=0
        Broker.__BROKER_ID+=1
        
    

    #A broker is responsible for a layer only
    # def __init__(self,network,resourceList:list,layerno) -> None:
    #     self.__network=network
    #     self.__brokerId=Broker.__BROKER_ID
    #     self.__deviceId=0
    #     self.__resourceList=resourceList
    #     Broker.__BROKER_ID+=1
        
        
    #This sets the work that needs to be given to the Broker
    def setResourceList(self,resourceList:list):
        self.__resourceList=resourceList
        self.__seq_pointer=0
    
    #This function sets the broker id for the device being used
    def __getBrokerDeviceId(self)->str:
        temp=f"#{self.__brokerId}_{self.__deviceId}"
        self.__deviceId+=1
        return temp
    
    #This function is responsible for assigning work to the instance of DeviceNode,Station,Mobile
    def assignLinearResources(self,device)->None:
        if self.isResourceEmpty():
            return 
        assert isinstance(device,DeviceNode)
        device.setResourceList(self.__resourceList[self.__seq_pointer])
        self.__seq_pointer+=1
        
    def startSimulation(self):
        if not(hasattr(self,self.__activeDevice)):
            self.getActiveDeviceState()
        time=0
        for device in self.__activeDevice:
            assert isinstance(device,DeviceNode)
            work=device.getResourceList()
            processingPower=device.getProcessingPower()
            time+=work/processingPower
        print("Total time taken:",time)
        return time

    # def getAllDeviceState():
    #     pass
    def getActiveDeviceState(self):
        network=self.__network
        assert isinstance(network,Network)
        layers=network.getNetworkLayers()
        self.__activeDevice=[]
        for layer in layers:
            assert isinstance(layer,Layer)
            for cluster in layer.getdeviceSpec_inLayer():
                for devices in cluster:
                    for device in devices:
                        assert isinstance(device,DeviceNode)
                        if device.getStatus==DeviceNode.READY:
                            self.__activeDevice.append(device)
            
    def ActiveDeviceStateSummary(self):
        self.AllDeviceStateSummary(onlyActive=True)
       

    def AllDeviceStateSummary(self,onlyActive:bool=False):
        network=self.__network
        assert isinstance(network,Network)
        layers=network.getNetworkLayers()
        for layer in layers:
            assert isinstance(layer,Layer)
            print(f"Layer-{layer.getLayerid()} State Summary".center(100," "))
            print(f"Device Id".center(20," ")+"|"+f"Type".center(20," ")+"|"+f"State".center(20," ")+"|"+f"Job".center(20," "))
            clusters=layer.getdeviceSpec_inLayer()
            for clusterno,cluster in enumerate(clusters):
                print(f"Cluster-{clusterno}".center(75," "))
                for devices in cluster:
                    for device in devices:
                        assert isinstance(device,DeviceNode)
                        id:str=f'{device.getDeviceId()}'.center(20," ")
                        status:int=device.getStatus()
                        if onlyActive and (status==DeviceNode.FAILED or status==DeviceNode.FAILED_RESOURCE_UNAVAILABLE or status==DeviceNode.CREATED):
                            continue
                        status:str=Broker.__state[status].center(20," ")
                        job=device.getResourceList()
                        if len(job)==0:
                            job="None".center(20," ")
                        else :
                            job=f"{job}".center(20," ")
                        if isinstance(device,Mobile):
                            type="Mobile"
                        else:
                            battery="None".center(20," ")
                        if isinstance(device,Station):
                            type="Station"
                        elif isinstance(device,DeviceNode):
                            type="Non Mobile"
                        type=type.center(20," ")
                        print(f"{id}|{type}|{status}|{job}")
            

    def resourceAllocationAlgorithm (self,algorithm=1):
        algo=Algorithm(self.__network,self,algorithm)
    
        

    def startSimulation():
        pass
    def deviceBreakDown(deviceObj):
        pass
    def updateDeviceStatus(deviceObj):
        pass
    def simualationSummary():
        pass

  
    def getResourceLength(self):
        return self.__resourceList

    def isResourceEmpty(self)->bool:
        if self.__seq_pointer!=len(self.__resourceList):
            return False
        return True
    def getInitialResourceList(self):
        return self.__resourceList


class Algorithm:

    _FCFS:int=1
    _COFFGA:int=2
    _CONFGA:int=3

    def __init__(self,network,broker,algorithm=1) -> None:
        print(algorithm)
        self.__network=network
        assert isinstance(self.__network,Network)
        self.__broker=broker
        assert isinstance(self.__broker,Broker)
        if algorithm == 1:
            self.FCFS()
        elif algorithm == 2:
            self.COFFGA()
        elif algorithm == 3:
            self.CONFGA()

        
        
    def FCFS(self):
        print("Allocating using FCFS")
        network=self.__network
        assert isinstance(network,Network)  
        broker=self.__broker
        assert isinstance(broker,Broker)
        no_Layers=network.getNumberofLayers()
        layers=network.getNetworkLayers()
        for layer in layers:
            assert isinstance(layer,Layer)
            clusters=layer.getdeviceSpec_inLayer()
            for cluster in clusters:
               for devices in cluster:
                   for device in devices:
                        assert isinstance(device,DeviceNode)
                        broker.assignLinearResources(device)
                        if broker.isResourceEmpty():
                         return 
    
    def COFFGA():
        pass
    def CONFGA():
        pass