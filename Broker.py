#This class is for allocating the resources and also is reponsible for the schdeduling algorithm used
#It assigns the broker id to the device when allocating the resources to it
from random import random
from attr import has
from sympy import minimum
from Cluster import Cluster
from Network import Network
from DeviceNode import DeviceNode
from Mobile import Mobile
from Station import Station
from Layer import Layer
from Task import Task
import random

class Broker:
    __BROKER_ID=0
    __state=["CREATED","READY","QUEUED","SUCCESS","FAILED","PAUSED","RESUMED","FAILED_RESOURCE_UNAVAILABLE"]

    
    def __init__(self,network) -> None:
        self.__network=network
        self.__brokerId=Broker.__BROKER_ID
        self.__deviceId=0
        self.dynamicAllocation=False
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
    
    #This function is responsible for assigning work to the instance of DeviceNode,Station,Mobile the task is assigned sequentially
    def assignLinearResources(self,device)->None:
        if self.isResourceEmpty():
            return 
        assert isinstance(device,DeviceNode)
        device.setResourceList(self.__resourceList[self.__seq_pointer])
        self.__seq_pointer+=1
    
 
        


    def getActiveDeviceState(self):
        network=self.__network
        assert isinstance(network,Network)
        layers=network.getNetworkLayers()
        self.__activeDevice=[]
        for layer in layers:
            assert isinstance(layer,Layer)
            for cluster in layer.getClusters():
                assert isinstance(cluster,Cluster)
                for device in cluster.getDevices():
                    assert isinstance(device,DeviceNode)
                    if device.getStatus==DeviceNode.READY:
                        self.__activeDevice.append(device)
            
    def ActiveDeviceStateSummary(self):
        self.AllDeviceStateSummary(onlyActive=True)
       

    def AllDeviceStateSummary(self,onlyActive:bool=False):
        if not(onlyActive):
            print(f" State of All Device Summary".center(100," "))
        else:
            print(f" State of Active Device Summary".center(100," "))
        network=self.__network
        assert isinstance(network,Network)
        layers=network.getNetworkLayers()
        for layer in layers:
            assert isinstance(layer,Layer)
            print(f"Layer-{layer.getId()} State Summary".center(100," "))
            print(f"Device Id".center(20," ")+"|"+f"Type".center(20," ")+"|"+f"State".center(20," ")+"|"+f"Job".center(20," "))
            clusters=layer.getClusters()
            for cluster in clusters:
                assert isinstance(cluster,Cluster)
                print(f"Cluster-{cluster.getId()}".center(75," "))
                for device in cluster.getDevices():
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
                        temp=[]
                        for a_job in job:
                            assert isinstance(a_job,Task)
                            temp.append(a_job.getInstructionLength())
                        job=temp
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
        

    def getUtilization(self):
        network=self.__network
        assert isinstance(network,Network)
        return network.getUtilization()
    
    def getUtilizationPerLayer(self):
        assert isinstance(self.__network,Network)
        return self.__network.getUtilzationPerLayer()
    
    def getUtilzationPerLayerPerCluster(self):
        assert isinstance(self.__network,Network)
        return self.__network.getUtilizationPerLayerPerCluster()*100

    def printUtilization(self):
        print("Network Utilzation = ",self.getUtilization())
    
    def printUtilizationPerLayer(self):
        assert isinstance(self.__network,Network)
        print('\n')
        printStr="Network Utilization Per Layer".center(100," ")
        print(printStr)
        for layer in self.__network.getNetworkLayers():
            assert isinstance(layer,Layer)
            print(f"Layer {layer.getId()} Utilization: {layer.getUtilzation()*100}")
    
    def printUtilizationPerLayerPerCluster(self):
        assert isinstance(self.__network,Network)
        print('\n')
        printStr="Network Utilization Per Cluster Per Layer".center(100," ")
        print(printStr)
        for layer in self.__network.getNetworkLayers():
            assert isinstance(layer,Layer)
            print(f"Layer {layer.getId()} Utilization".center(100," "))
            printStr=""
            printStr2=""
            for cluster in layer.getClusters():
                assert isinstance(cluster,Cluster)
                printStr2+=("Cluster "+str(cluster.getId())).center(20," ")
                printStr+=(str(cluster.getUtilization()*100)+"%").center(20," ")
        print(printStr2)
        print(printStr)



        


            

    # def resourceAllocationAlgorithm (self,algorithm=1):
    #     self.__algo=Algorithm(self.__network,self)
    #     self.__algo.resourceAllocation(algorithm)
    
    # def loadbalancing(self,algorithm):
    #     if not(hasattr(self,"_Broker__algorithm")):
    #         print("Error:No prior allocation of task")
    #         return-
    #     self.__algo.loadbalancing()

    
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

    def startsimulation(self):
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

    _RoundRobin:int=1
    _COFFGA:int=2
    _CONFGA:int=3
    _WeightedRoundRobin:int=4
    _randomAllocation:int=5

    def __init__(self,network,broker) -> None:

        self.__network=network
        assert isinstance(self.__network,Network)
        self.__broker=broker
        assert isinstance(self.__broker,Broker)

    
    def resourceAllocation(self,algorithm=1):
        if algorithm == Algorithm.RoundRobin:
            self.RoundRobin()
        elif algorithm == Algorithm.COFFGA:
            self.COFFGA()
        elif algorithm == Algorithm._CONFGA:
            self.CONFGA()
        elif algorithm==Algorithm._WeightedRoundRobin:
            self.WeightedRoundRobin()
        elif algorithm==Algorithm._randomAllocation:
            self.randomAllocation()
        else:
            print('Error:Allocation Algorithm not present')
    
  


        
        
    def RoundRobin(self):
        print("Allocating using Round Robin")
        network=self.__network
        assert isinstance(network,Network)  
        broker=self.__broker
        assert isinstance(broker,Broker)
        no_Layers=network.getNumberofLayers()
        layers=network.getNetworkLayers()
        #Allocating Tasks only if the devices doesnt have any task
        for layer in layers:
            assert isinstance(layer,Layer)
            for cluster in layer.getClusters():
                assert isinstance(cluster,Cluster)
                for device in cluster.getDevices():
                    assert isinstance(device,DeviceNode)
                    if device.getStatus() == DeviceNode.CREATED:
                        broker.assignLinearResources(device)
                    if broker.isResourceEmpty():
                        return 
        #If task remains , the task is allocated to the very first device in the layer
        if not(broker.isResourceEmpty):
            for layer in layers:
                assert isinstance(layer,Layer)
                for cluster in layer.getClusters():
                    assert isinstance(cluster,Cluster)
                    for device in cluster.getDevices():
                        assert isinstance(device,DeviceNode)
                        broker.assignLinearResources(device)
                        if broker.isResourceEmpty():
                         return
    
    def WeightedRoundRobin(self):
        print("Allocation using Weighted Round Robin")
        network=self.__network
        broker=self.__broker
        assert isinstance(broker,Broker) and isinstance(network,Network)
        firstLayer=network.getNetworkLayers()[0]
        assert isinstance(firstLayer,Layer)
        clusterList=firstLayer.getClusters()
        minimum=-1
 
        #Calculating the processing power per cluster and finding the minimum processing power in a cluster
        for cluster in clusterList:
            assert isinstance(cluster,Cluster)
            temp=0
            for device in cluster.getDevices():
                assert isinstance(device,DeviceNode)
                temp=temp+device.getProcessingPower()
            if minimum==-1:
                minimum=temp
            cluster.setWeight(temp)
        #We set the weight (processing power /minimum processing power)
        for cluster in clusterList:
            assert isinstance(cluster,Cluster)
            cluster.setWeight(round(cluster.getWeight()/minimum))
        #Sorting of cluster based on cluster weight
        for i in range(len(clusterList)):
            for j in range(i+1,len(clusterList)):
                clusterA=clusterList[i]
                clusterB=clusterList[j]
                assert isinstance(clusterA,Cluster) and isinstance(clusterB,Cluster)
                if clusterA.getWeight()<clusterB.getWeight():
                    temp=clusterA
                    clusterA=clusterB
                    clusterB=temp
        #Assigning of task based on weight
        while( not(broker.isResourceEmpty())):
            for cluster in clusterList:
                assert isinstance(cluster,Cluster)
                devices=cluster.getDevices()
                i=0
                j=0
                while (i < cluster.getWeight() ):
                    broker.assignLinearResources(devices[j])
                    j+=1
                    i+=1
                    if not(j<len(devices)):
                        j=0
    
    def randomAllocation(self):
        network=self.__network
        broker=self.__broker
        assert isinstance(broker,Broker)
        assert isinstance(network,Network)
        firstLayer=network.getNetworkLayers()[0]
        assert isinstance(firstLayer,Layer)
        clusters=firstLayer.getClusters()
        while(not(broker.isResourceEmpty())):
            temp=random.randint(0,len(clusters))
            randomCluster=clusters[temp]
            assert isinstance(randomCluster,Cluster)
            randomDevice=random.randint(0,len(randomCluster.getDevices()))
            assert isinstance(randomDevice,DeviceNode)
            broker.assignLinearResources(randomDevice)

        



        
    



                

            
        

            



        

            
            


       



    


    

    #The offloading stratergies are encoded in a general algorithm
    #Offloading stratergy sorted by the number of empty vm instances capable of processing task in descending order
    #Task offloaded to the first Edge node that has required empty Vm for the task
    #The same condition for the other task
    def COFFGA():
        pass
    
    #Selection process same of COFFGA
    #When Searching for suitable EdgeNode, the location of the EdgeNode is recorded for offloading next task
    def CONFGA():
        pass

    def iterativeBalance(self):
        cluster=self.__network
        
        for i in range(1000):
            pass