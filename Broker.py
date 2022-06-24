
from ClusterParallelization import ClusterParallelization
from Network import Network,Layer,Cluster,DeviceNode,Mobile,Station
from Task import Task
from TaskGenerator import TaskGenerator
import random
import copy
from Chromosome import Chromosome
from ChromosomeCopy import ChromosomeCopy
from threading import Thread
import time
import Graph
class Broker:
    """
    Class that tracks the network\n
    Also  for allocating the resources and also is reponsible for the scheduling algorithm used\n
    Has a method to keep track of device status\n
    It assigns the broker id to the device when allocating the resources to it\n
    """
    __BROKER_ID=0
    __state=["CREATED","READY","QUEUED","SUCCESS","FAILED","PAUSED","RESUMED","FAILED_RESOURCE_UNAVAILABLE"]

    
    def __init__(self,network) -> None:
        self.__network=network
        self.__brokerId=Broker.__BROKER_ID
        self.__deviceId=0
        self.dynamicAllocation=False
        self.__resourceList=[]
        self.__allocatedTask=[]
        self.__algorithm=""
        self.__algo=None
        self.__table={}
        self.__hasAllocated=False
        self.deviceStatusinfo_Flag=False

        
        Broker.__BROKER_ID+=1
        assert isinstance(self.__network,Network)

    

    #A broker is responsible for a layer only
    # def __init__(self,network,resourceList:list,layerno) -> None:
    #     self.__network=network
    #     self.__brokerId=Broker.__BROKER_ID
    #     self.__deviceId=0
    #     self.__resourceList=resourceList
    #     Broker.__BROKER_ID+=1
        
        
    def setResourceList(self,resourceList:list):
        """
        Sets the work that needs to be given to the Broker
        """
        self.__resourceList=resourceList
        self.__seq_pointer=0
    
    def getBrokerId(self):
        """Returns the broker id """
        return self.__brokerId

    def __getBrokerDeviceId(self)->str:
        """
        This function sets the broker id for the device being used
        """
        temp=f"#{self.__brokerId}_{self.__deviceId}"
        self.__deviceId+=1
        return temp
    
    
    def assignLinearResources(self,device)->None:
        """
        This function is responsible for assigning work to the instance\n
        of DeviceNode,Station,Mobile the task is assigned sequentially
        """
        if self.isResourceEmpty():
            return 
        assert isinstance(device,DeviceNode)
        device.setResourceList(self.__resourceList[self.__seq_pointer])
        self.__allocatedTask.append(self.__resourceList[self.__seq_pointer])
        print(f"\nAllocating task {self.__resourceList[self.__seq_pointer]} to device {device.getDeviceId()}")
        self.__seq_pointer+=1
    
    def assignResourcesChromosome(self,chromosome:Chromosome) ->None:
        """
        Allocates the task based on the chromosome structure
        """
        assert isinstance(self.__network,Network)
        for sectionNo,section in enumerate(chromosome.getSections()):
            assert isinstance(section,Chromosome.Chormosome_section)
            for unitNo,unit in enumerate(section.getUnits()):
                assert isinstance(unit,Chromosome.Chormosome_section.Chromosome_unit)
                output=[]
                for x in unit.getTasks():
                    output.append(x)
                if unit.getTasks():
                    for task in unit.getTasks():
                        layer=self.__network.getNetworkLayers()[0]
                        cluster=layer.getClusters()[sectionNo]
                        device=cluster.getDevices()[unitNo]
                        assert isinstance(device,DeviceNode)
                        device.setResourceList(task)
                        # print(f'allocating {task} to {device}')
                        
        # for clusterno,cluster in enumerate(chromosome):
        #     for deviceno,device in enumerate(cluster):
        #         if device ==1:
        #             obj=self.__network.getNetworkLayers()[0].getClusters[clusterno].getDevices[deviceno]
        #             self.assignLinearResources(obj)


    def updateSeqPointer(self,value):
        """Pointer responsible for keeping track of allocated jobs"""
        self.__seq_pointer=value
    def getActiveDeviceState(self):
        """
        It appends all the active device into the __activeDevice varaible
        """
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
        """
        Outputs only the active device in the network in a table format
        """
        self.allDeviceStateSummary(onlyActive=True)
       

    def allDeviceStateSummary(self,onlyActive:bool=False):
        """
        Outputs all the device and its status, and type in table format
        """
        print('\n\n')
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
                            temp.append(a_job.getId())
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

    def setAlgorithm(self,algorithm):
        self.__algorithm=algorithm
    def getAlgorithm(self):
        return self.__algorithm
    def getAlgoObject(self):
        return self.__algo
    
    def getUtilization(self):
        """Gets the utilization of the overall network\n
           Utilization of the network from the Network instance's method\n        
        """
        network=self.__network
        assert isinstance(network,Network)
        return network.getUtilization()
    
    def getUtilizationPerLayer(self):
        """Gets the utilization of the overall network\n
           Utilization of the network from the Network instance's method\n        
        """
        assert isinstance(self.__network,Network)
        return self.__network.getUtilzationPerLayer()
    
    def getUtilzationPerLayerPerCluster(self):
        """Gets the utilization of each layer \n
           Utilization of the network from the Network instance's method\n        
        """
        assert isinstance(self.__network,Network)
        return self.__network.getUtilizationPerLayerPerCluster()*100

    def printUtilization(self):
        """Prints the utilizaiton of the overall network"""
        print("Network Utilzation = ",self.getUtilization())
    
    def printUtilizationPerLayer(self):
        """Prints the utilization of each layer """
        assert isinstance(self.__network,Network)
        print('\n')
        printStr="Network Utilization Per Layer".center(100," ")
        print(printStr)
        for layer in self.__network.getNetworkLayers():
            assert isinstance(layer,Layer)
            print(f"Layer {layer.getId()} Utilization: {layer.getUtilzation()*100}")
    
    def printUtilizationPerLayerPerCluster(self):
        """Prints the utilization of each cluster in each layer"""
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

    def addTasks(self,tasks):
        self.__resourceList.extend(tasks)
 

    def resourceAllocationAlgorithmStatic(self,algorithm=1):
        """Allocates the task based on the Algorithm\n
           if the allocation technique is dynamic,a thread needs to be associated while allocating\n
        """
        if self.isResourceEmpty():
            print(f"No Tasks to allocate, but called {__name__}")
            return
        self.setAlgorithm(algorithm)
        self.__algo=Algorithm(self.__network,self)
        self.__algo.resourceAllocation(algorithm)
        self.__hasAllocated=True


    def printWeightNetwork(self):
        """Prints the weight of the network\n
           The weight of the network is based\n
           on the processing power as of now
        """

        if hasattr(self,'_Broker__algo'):
            assert isinstance(self.__algo,Algorithm)
            algorithm=self.__algo.getAlgorithm()
            if algorithm==Algorithm._WeightedRoundRobin:
                print('\n')
                print("Weight of the Network".center(100," "))
                network=self.__network
                assert isinstance(network,Network)
                for layer in network.getNetworkLayers():
                    assert isinstance(layer,Layer)
                    print(f"Layer-{layer.getId()}".center(100," "))
                    printStr=""
                    for cluster in layer.getClusters():
                        assert isinstance(cluster,Cluster)
                        printStr+=f'Cluster-{cluster.getId()}: {cluster.getWeight()}'.center(20," ")
                    print(printStr)
        else:
            print('\n')
            print("Error:No weighted algorithm used")
        return
    
    def loadbalancing():
         pass
  
    
    def startStaticSimulation(self):
        """Starts the simulation and calculates the time using arithmetic of job/processing_power\n
           This simulation doesn't use any threading and parellization \n
        """
        network=self.__network
        assert isinstance(network,Network)
        layer0=network.getNetworkLayers()[0]
        assert isinstance(layer0,Layer)
        clusterTimeList=[]
        for cluster in layer0.getClusters():
            deviceTimeList=[]
            assert isinstance(cluster,Cluster)
            for device in cluster.getDevices():
                assert isinstance(device,DeviceNode)
                time=0
                for task in device.getResourceList():
                    assert isinstance(task,Task)
                    job=task.getInstructionLength()
                    time+=(job/device.getProcessingPower())
                deviceTimeList.append(time)
            maximum=max(deviceTimeList)
            clusterTimeList.append(maximum)
        return max(clusterTimeList)

                


    def resetTaskAllocated(self):
        """
        Resets the tasks allocated to the devices\n
        Making the task queue of the device to empty\n
        """
        assert isinstance(self.__network,Network)
        self.__network.resetTaskAllocated()
        self.__seq_pointer=0
        self.__hasAllocated=False

    
    def setRoundRobinPointer(self,device:DeviceNode):
        """Keeps a track of which device to allocate from and to\n
           maintain  the flow of allocation during roundRobin\n
           Calls the algorithm instance's setRoundRObinPointer method \n
        """
        if hasattr(self,'_Broker__algo'):
            assert isinstance(self.__algo,Algorithm)
            self.__algo.setRoundRobinPointer(device)

  
    def getResourceLength(self):
        """Returns the length of the resource/tasks"""
        return len(self.__resourceList)

    def isResourceEmpty(self)->bool:
        """Checks if the resources if empty"""
        if len(self.__resourceList)==0:
            return True
        if self.__seq_pointer>=self.getResourceLength():
            return True
        return False
    def getResourceList(self):
        """Returns the task list from the broker instance"""
        return self.__resourceList
    
    def getNetwork(self):
        """Returns the network instance associated with the broker"""
        return self.__network
    
    def ga_vs_lot(self):
        broker=self
        network=self.__network
        algo=Algorithm(network,broker)
        lotlist,timelist=algo.ga(test=True)
        print('lotlist',lotlist)
        print('timelist',timelist)
        graph=Graph.Graph()
        graph.plotBarGraph(values=timelist,names=lotlist,title='lotsize vs time',xlabel='lotsize',ylabel='time taken')

    def deviceBreakDown(deviceObj):
        pass
    def updateDeviceStatus(deviceObj):
        pass
    def simualationSummary():
        pass
    def getTaskList(self):
        return self.__resourceList
        

    def getDeviceStatusinfo(self,network,t=0.3,flag=False):
       """ 
       Used with multithreading\n
       Function gets the Device Status info\n
       Takes network and time(t) as parameter\n
       the default sleep time(t)=1\n
       """
       self.deviceStatusinfo_Flag=flag

       if not(self.deviceStatusinfo_Flag):
           print("deviceStatusInfo Flag is set to False")
           return

       assert isinstance(network,Network)
       layer0=network.getNetworkLayers()[0]
       clusters=layer0.getClusters()
       while(self.deviceStatusinfo_Flag):
        for cluster in clusters:
            for device in cluster.getDevices():
                status=device.getStatusText()
                print(f"\nDeivce {device.getDeviceId()}: {status}",end="\t")
            print("\n")
            time.sleep(t)

    def check_Update_Parallelization(self,clusterParallelObjects,isResrouceEmpty):
        """
        Takes  list of ClusterParallelObject (ClusterParallelObjects) as a parameter\n 
        if there is no task in a clusterParallelObject, it stops the \n
        the parallelizaiton of that clusterParallelObject\n
        """
        while(True):
            # print("\nCheckupdate",isResrouceEmpty())
            if not(isResrouceEmpty()):
                time.sleep(2)
                continue
            clusterPobj_Status=[[obj,obj.taskCheck()]  for obj in clusterParallelObjects]
            lister=[item[1] for item in clusterPobj_Status]
            # print(clusterPobj_Status)
            for items in clusterPobj_Status:
                clustertemp=items[0]
                assert isinstance(clustertemp,ClusterParallelization)
                if items[1]==False:
                    clustertemp.stopParallelization()
            if not(any(lister)):
                 break
            time.sleep(2)

        if self.__algorithm==Algorithm._DynamicAlgorithm:
            if hasattr(self.__algo,"stopDynamicAlgorithm"):
                self.__algo.stopDynamicAlgorithm=True
                print("stopping dynamic Algorithm ")
        print("Cluster Status Update is terminated")




    def startSimulation(self,result):
        """
        Starts the simulation based on cluster Parallelizaion\n
        it appends the results of the time taken by the simulation\n
        """
        print("[STARTING] Simulation")
        clusterThreads=[]
        clusterParallelobj=[]
        network=self.__network
        assert isinstance(network,Network)
        layer0=network.getNetworkLayers()[0]
        assert isinstance(layer0,Layer)
        clusters=layer0.getClusters()
        #Creating ClusterParallelization object
        self.isThereTask_Flag=self.isResourceEmpty()

        for cluster in clusters:
            cluster_Pobj=ClusterParallelization(cluster)
            clusterParallelobj.append(cluster_Pobj)
        #Assigning each clusterParallelization object to a thread, allows each cluster
        #to have concurrent execution
        for cluster in clusterParallelobj:
            assert isinstance(cluster,ClusterParallelization)
            thread=Thread(target=cluster.clusterParallelization)
            clusterThreads.append(thread)

        #Here we add another thread to check if the broker has task 
        #if so we allocate the task using a given allocatino algorithm

        #we add another thread to take dynamic input 
        #like keep adding task 
        t1=Thread(target=self.check_Update_Parallelization,args=(clusterParallelobj,self.isResourceEmpty))
        timestart=time.perf_counter()
        for thread in clusterThreads:
            thread.start()
        t1.start()
        for thread in clusterThreads:
            thread.join()
        t1.join()
        timeend=time.perf_counter()
        result.append((timeend-timestart))
       
        
        print("\n[TERMINATING] Simulation")



    def startDynamicSimuation(self):
        """
        This function creates Parallelization based on threads\n
        Clusters run parallely using threads, concurrent execution of the cluster\n
        Cluster Parallelizaiton is a class which allows device parallelziation in a cluster\n
        as the devices in the cluster needs to run concurrently, for proper simulation\n
        This is limited by the device specification as a big network will create lot of \n
        threads for the simulation of the network\n
        """
        print("[STARTING] Dynamic Simulation")
        clusterThreads=[]
        clusterParallelobj=[]
        network=self.__network
        assert isinstance(network,Network)
        layer0=network.getNetworkLayers()[0]
        assert isinstance(layer0,Layer)
        clusters=layer0.getClusters()
        #Creating ClusterParallelization object
        for cluster in clusters:
            cluster_Pobj=ClusterParallelization(cluster)
            clusterParallelobj.append(cluster_Pobj)
        #Assigning each clusterParallelization object to a thread, allows each cluster
        #to have concurrent execution
        for cluster in clusterParallelobj:
            assert isinstance(cluster,ClusterParallelization)
            thread=Thread(target=cluster.clusterParallelization)
            clusterThreads.append(thread)

        #Here we add another thread to check if the broker has task 
        #if so we allocate the task using a given allocatino algorithm

        #we add another thread to take dynamic input 
        #like keep adding task 

        
        for thread in clusterThreads:
            thread.start()
        for thread in clusterThreads:
            thread.join()
      

                
            

    
            
      


  
 
          
          

            
        




        


        
              
            
            



class Algorithm:
    """
    A class for the allocation stratergies that can be used for the network\n
    """

    _RoundRobin:int=1
    _COFFGA:int=2
    _CONFGA:int=3
    _WeightedRoundRobin:int=4
    _RandomAllocation:int=5
    _GA:int=6
    _DynamicAlgorithm:int=7

    def __init__(self,network,broker) -> None:

        self.__network=network
        assert isinstance(self.__network,Network)
        self.__broker=broker
        assert isinstance(self.__broker,Broker)
        self.__algorithm=-1
        self.__roundRobinPointer=None

    
    def resourceAllocation(self,algorithm=1):
        """Method for allocting tasks based on an algorithm\n
           Tells which algorithm to execute based on the class variable\n
           associated with the algorithms
        """
        self.__algorithm=algorithm
        if algorithm == Algorithm._RoundRobin:
            self.roundRobin()
        elif algorithm == Algorithm._COFFGA:
            self.coffga()
        elif algorithm == Algorithm._CONFGA:
            self.confga()
        elif algorithm==Algorithm._WeightedRoundRobin:
            self.weightedRoundRobin()
        elif algorithm==Algorithm._RandomAllocation:
            self.randomAllocation()
        elif algorithm ==Algorithm._GA:
            self.ga()
        elif algorithm==Algorithm._DynamicAlgorithm:
            self.dynamicAlgorithm()
        else:
            print('Error:Allocation Algorithm not present')
    
  


    def setRoundRobinPointer(self,device:DeviceNode):
        """Keeps a track of which device to allocate from and to\n
            maintain  the flow of allocation during roundRobin\n
        """
        self.__roundRobinPointer=device


    #Need for a roundrobin pointer that tracks the last device that was set with tasks
    def roundRobin(self):
        """Allocates the task based on Round Robin method\n
           Allocation based on the serial no starting from the first to last \n
           and then iterates again , until the all the task are allocated\n
        """
        print("Allocating using Round Robin")
        network=self.__network
        assert isinstance(network,Network)  
        broker=self.__broker
        assert isinstance(broker,Broker)
        no_Layers=network.getNumberofLayers()
        layers=network.getNetworkLayers()
        layer0=layers[0]
        assert isinstance(layer0,Layer)

        #when roundrobinpinter is None : make isdevicefound=true
        #this removes the need for checking is roundrobinPointer is not None
        #Makes the function more generic
        def assignTask():  
            isdeviceFound=False
            if self.__roundRobinPointer==None:
                isdeviceFound=True
            while( not(broker.isResourceEmpty())):
                for cluster in layer0.getClusters():
                    assert isinstance(cluster,Cluster)
                    for device in cluster.getDevices():
                        assert isinstance(device,DeviceNode)
                        if isdeviceFound:
                            broker.assignLinearResources(device)
                            self.__roundRobinPointer=device
                        if not(isdeviceFound) and  device== self.__roundRobinPointer:
                            isdeviceFound=True
                        if broker.isResourceEmpty():
                            return

                            
        # assignWhenPointerNone()
        assignTask()
            

       






 
        


    
  
    
    def weightedRoundRobin(self):
        """Allocation based on weighted Round Robin \n
           Weight is calculated based on the processing power of the cluster\n
           Greater the weight more the task is allocated to the cluster\n
           
           Ex:  cluster 1 weight=1 ,cluster2  weight=2\n
                cluster task is allocated twice the task to cluster 1\n
        """
        print("Allocation using Weighted Round Robin")
        network=self.__network
        broker=self.__broker
        assert isinstance(broker,Broker) and isinstance(network,Network)
        firstLayer=network.getNetworkLayers()[0]
        assert isinstance(firstLayer,Layer)
        clusterList=[]
        for cluster in firstLayer.getClusters():
            clusterList.append(cluster)
        
      
        def calculateWeight():
            """
            Calculating the processing power per cluster and finding the minimum processing power in a cluster
            """
            minimum=-1
            for cluster in clusterList:
                assert isinstance(cluster,Cluster)
                processingPower=0
                for device in cluster.getDevices():
                    assert isinstance(device,DeviceNode)
                    processingPower=processingPower+device.getProcessingPower()
                if minimum==-1:
                    minimum=processingPower
                if minimum > processingPower:
                    minimum=processingPower
                cluster.setWeight(processingPower)

            for cluster in clusterList:
                """
                Set the weight (processing power /minimum processing power)
                """
                assert isinstance(cluster,Cluster)
                cluster.setWeight(round(cluster.getWeight()/minimum))

        def sortingClusterbyWeight():
            """ Sorting of cluster based on cluster weight """
            for i in range(len(clusterList)):
                for j in range(i+1,len(clusterList)):
                    if clusterList[i].getWeight()<clusterList[j].getWeight():
                        temp=clusterList[i]
                        clusterList[i]=clusterList[j]
                        clusterList[j]=temp
                    if clusterList[i].getWeight()==clusterList[j].getWeight():
                        if clusterList[i].getId()>clusterList[j].getId():
                            temp=clusterList[i]
                            clusterList[i]=clusterList[j]
                            clusterList[j]=temp

                
            

        def assignTask():
            """Assigning of task based on weight"""
            while( not(broker.isResourceEmpty())):
                for cluster in clusterList:
                    assert isinstance(cluster,Cluster)
                    devices=cluster.getDevices()
                    weight=0 #This reponsible for the loop (giving the weightage for the cluster)
                    while (weight< cluster.getWeight() ):
                        allocationDirection=[]
                        for device in devices:
                            allocationDirection.append(device)
                        
                        for i in range(len(allocationDirection)):
                            for j in range(i+1,len(allocationDirection)):
                                if len(allocationDirection[i].getResourceList())>len(allocationDirection[j].getResourceList()):
                                    temp=allocationDirection[i]
                                    allocationDirection[i]=allocationDirection[j]
                                    allocationDirection[j]=temp
                                
                                if len(allocationDirection[i].getResourceList()) ==len(allocationDirection[j].getResourceList()):
                                    if allocationDirection[i].getDeviceId()>allocationDirection[j].getDeviceId():
                                            temp=allocationDirection[i]
                                            allocationDirection[i]=allocationDirection[j]
                                            allocationDirection[j]=temp

                        for device in allocationDirection:
                            broker.assignLinearResources(device)
                            weight+=1
                            if broker.isResourceEmpty():
                                return
                            if weight>=cluster.getWeight():
                                break
                            

        calculateWeight()
        sortingClusterbyWeight()
        assignTask()



    
    def randomAllocation(self):
        """Allocation of the task based randomly\n
           First gets a random cluster then gets \n
           a random device in that cluster and allocates\n
        """
        print("Allocation using Random Allocation ")
        network=self.__network
        broker=self.__broker
        assert isinstance(broker,Broker)
        assert isinstance(network,Network)
        firstLayer=network.getNetworkLayers()[0]
        assert isinstance(firstLayer,Layer)
        clusters=firstLayer.getClusters()
        while(not(broker.isResourceEmpty())):
            randomCluster=random.randint(0,len(clusters)-1)
            randomCluster=clusters[randomCluster]
            assert isinstance(randomCluster,Cluster)
            randomDevice=random.randint(0,len(randomCluster.getDevices())-1)
            randomDevice=randomCluster.getDevices()[randomDevice]
            assert isinstance(randomDevice,DeviceNode)
            broker.assignLinearResources(randomDevice)

    

    #The offloading stratergies are encoded in a general algorithm
    #Offloading stratergy sorted by the number of empty vm instances capable of processing task in descending order
    #Task offloaded to the first Edge node that has required empty Vm for the task
    #The same condition for the other task
    def coffga():
        pass
    
    #Selection process same of COFFGA
    #When Searching for suitable EdgeNode, the location of the EdgeNode is recorded for offloading next task
    def confga():
        pass

    def iterativeBalance(self):
        cluster=self.__network
        
        for i in range(1000):
            pass
    
    def ga(self,gernerationLimit:int=20,lotsize=10,test=False):
        """Allocation based on Genetic algorithm (GA)\n
           GA gets the random population,mutates ,then undergeoes\n
           selection and then new poplulation is selected\n
           
           takes generation limit and lot size as parameter\n
        """
        print("Allocation using Genetic Algorithm ")
        broker=self.__broker
        assert isinstance(broker,Broker)
        network=self.__network
        assert isinstance(network,Network)
        layer=network.getNetworkLayers()[0]
        assert isinstance(layer,Layer)
        clusters=layer.getClusters()
        len_clusters=len(clusters)
        processingTime=0
        allocatingList=[]
        

        def printChromosomeCounter(chromosomes):
            """
            Prints the number of task allocated to a device in a section
            """
            for chromosome in chromosomes:
                assert isinstance(chromosome,Chromosome)
                print("Chromosome",chromosome.getId())
                data=[]
                for section in chromosome.getSections():
                    assert isinstance(section,Chromosome.Chormosome_section)
                    datasection=[]
                    for unit in section.getUnits():
                        assert isinstance(unit,Chromosome.Chormosome_section.Chromosome_unit)
                        taskcounter=0
                        for task in unit.getTasks():
                            taskcounter+=1
                        datasection.append(taskcounter)
                    data.append(datasection)
                print(data)
     

        def printChromosomeTaskId(chromosomes):
            """
               prints the the task obj details in the device of a section
            """
            for chromosome in chromosomes:
                assert isinstance(chromosome,Chromosome)
                print("Chromosome",chromosome.getId())
                data=[]
                for section in chromosome.getSections():
                    assert isinstance(section,Chromosome.Chormosome_section)
                    datasection=[]
                    for unit in section.getUnits():
                        assert isinstance(unit,Chromosome.Chormosome_section.Chromosome_unit)
                        for task in unit.getTasks():
                            datasection.append(task.getId())
                    data.append(datasection)
                print(data)       
       

        def generateRandomChromosomes(no=lotsize):
            """
             generates a sample size of chromosomes
            """
            # print("Generating pool of random Chromosome")
            chromosomeList=[]
            #Chromosome is network equivalent,section is cluster equivalent,unit is device equivalent
            for i in range(no):
                chromosome=Chromosome()
                chromosome.creationViaLayer(layer)
                for task in broker.getTaskList():
                    randomSection=random.randint(0,len(chromosome.getSections())-1)
                    randomSection=chromosome.getSections()[randomSection]
                    randomUnit=random.randint(0,len(randomSection.getUnits())-1)
                    randomUnit=randomSection.getUnits()[randomUnit]
                    randomUnit.setTask(task)
                chromosomeList.append(chromosome)
            return chromosomeList
       
        def calculateChromosome(chromosomeList):
            """
            Function for calculating the time taken for the allocation stratergy of the encoded chromosome
            """
            network=Network()
            network.copyNetwork(self.__network)
            tempbroker=Broker(network)
            for chromosome in chromosomeList:
                assert isinstance(chromosome,Chromosome)
                tempbroker.resetTaskAllocated()
                tempbroker.assignResourcesChromosome(chromosome)
                time=tempbroker.startStaticSimulation()
                chromosome.setTime(time)


        def mutatation(chrmoList)->list[list[int]]:
            """
            Function for that mutates the chromosome with mutation and crossover operators
            """
            chromosomes=[]
            for chrmo in chrmoList:
                assert isinstance(chrmo,Chromosome)
                chrmoObj=ChromosomeCopy.copy(chrmo)
                chromosomes.append(chrmoObj)
            
            
            
            def crossover():
                """
                swaps a allocated task if any with another task if any within a chromosome
                """
                # print("Undergoing crossover of the Chromosome")
                crossoverRange=4
                for chromosome in chromosomes:
                    for i in range(crossoverRange):
                        randomSection_A=random.randint(0,len(chromosome.getSections())-1)
                        randomSection_B=random.randint(0,len(chromosome.getSections())-1)
                        randomSection_A=chromosome.getSections()[randomSection_A]
                        randomSection_B=chromosome.getSections()[randomSection_B]
                        randomUnit_A=random.randint(0,len(randomSection_A.getUnits())-1)
                        randomUnit_A=randomSection_A.getUnits()[randomUnit_A]
                        randomUnit_B=random.randint(0,len(randomSection_B.getUnits())-1)
                        randomUnit_B=randomSection_B.getUnits()[randomUnit_B]
                        if randomSection_A is randomSection_B:
                            #Allows an iteration to not compulsarily mutate
                            if randomUnit_A is randomUnit_B:
                                continue
                            #Below would force a absolute event of mutation to occur 
                            # while (randomUnit_A is randomUnit_B):
                            #     randomUnit_B=random.randint(0,len(randomSection_B.getUnits())-1)
                            #     randomUnit_B=randomSection_B.getUnits()[randomUnit_B]
                        assert isinstance(randomUnit_A,Chromosome.Chormosome_section.Chromosome_unit)
                        assert isinstance(randomUnit_B,Chromosome.Chormosome_section.Chromosome_unit)
                        randomTask_A=[]
                        randomTask_B=[]
                        #After we get refrence to the task we remove it from the list of the Chromosome.Chromosome_Unit.__task
                        if len(randomUnit_A.getTasks())>0:
                            randomTask_A=random.randint(0,len(randomUnit_A.getTasks())-1)
                            randomTask_A=randomUnit_A.getTasks()[randomTask_A]
                            # print('TaskA',type(randomTask_A),randomTask_A)
                            assert isinstance(randomTask_A,Task)
                            randomUnit_A.getTasks().remove(randomTask_A)
                        if len(randomUnit_B.getTasks())>0:
                            randomTask_B=random.randint(0,len(randomUnit_B.getTasks())-1)
                            randomTask_B=randomUnit_B.getTasks()[randomTask_B]
                            # print('TaskB',type(randomTask_B),randomTask_B)
                            assert isinstance(randomTask_B,Task)
                            randomUnit_B.getTasks().remove(randomTask_B)
                        #Swapping of the task
                        if isinstance(randomTask_A,list) and isinstance(randomTask_B,Task):
                            randomUnit_A.setTask(randomTask_B)
                        elif isinstance(randomTask_A,Task) and isinstance(randomTask_B,list):
                            randomUnit_B.setTask(randomTask_A)
                        elif isinstance(randomTask_A,Task) and isinstance(randomTask_B,Task):
                            randomUnit_A.setTask(randomTask_B)
                            randomUnit_B.setTask(randomTask_A)
                # print("Crossover Complete")

          
            def mutate():
                """
                  With a probabilty of 25% chance of deleting a task from a device and adding it to another device within a chromosome
                """
                # print("Undergoing mutation of the Chromosome")
                mutateRange=3
                for chromosome in chromosomes:
                    assert isinstance(chromosome,Chromosome)
                    for i in range(mutateRange):
                        #Possibilty of deleting a task or not
                        flag=random.randint(0,3)
                        #probabilty of not mutating 3/4=75% , if flag ==3 we mutate
                        if flag==3:
                            randomSection=random.randint(0,len(chromosome.getSections())-1)
                            randomSection=chromosome.getSections()[randomSection]
                            assert isinstance(randomSection,Chromosome.Chormosome_section)
                            randomUnit=random.randint(0,len(randomSection.getUnits())-1)
                            randomUnit=randomSection.getUnits()[randomUnit]
                            assert isinstance(randomUnit,Chromosome.Chormosome_section.Chromosome_unit)
                            if randomUnit.getTasks():
                                task=random.randint(0,len(randomUnit.getTasks())-1)
                                task=randomUnit.getTasks()[task]
                                assert isinstance(task,Task)
                                randomUnit.getTasks().remove(task)
                                #Randomly adding the deleted task to some device
                                randomSection=random.randint(0,len(chromosome.getSections())-1)
                                randomSection=chromosome.getSections()[randomSection]
                                assert isinstance(randomSection,Chromosome.Chormosome_section)
                                randomUnit=random.randint(0,len(randomSection.getUnits())-1)
                                randomUnit=randomSection.getUnits()[randomUnit]
                                assert isinstance(randomUnit,Chromosome.Chormosome_section.Chromosome_unit)
                                randomUnit.setTask(task)
                # print('Mutation complete')
            mutate()
            crossover()
            # print("Mutation Done")
            # print(chromosomes)
            # print("\n")
            return chromosomes
            #end of muatation()
        
    
        def mergePopulation(parent:list[Chromosome],child:list[Chromosome]):
            """
            Merging the child and parent chromosome 
            """
            chromosomes=[]
            chromosomes.extend(parent)
            chromosomes.extend(child)
            return chromosomes



        
        def binaryTournamentSelection(poption):
            """Selection based on binary tournament selction \n
               Random pair of chromosomes are selected and the better one is the winner\n
               The winners of each pair battle is returned\n
            """
            population=copy.deepcopy(poption)
            survival=[]
            if len(population)<2:
                return population
            
            while(len(population)>=2):
                p1=random.randint(0,len(population)-1)
                p1=population[p1]
                population.remove(p1)
                p2=random.randint(0,len(population)-1)
                p2=population[p2]
                population.remove(p2)
                assert isinstance(p1,Chromosome) and isinstance(p2,Chromosome)
                # print(p1,"vs",p2)
                if p1.getTime()<p2.getTime():
                    # print(f"{p1} wins")
                    survival.append(p1)
                elif p2.getTime()<p1.getTime():
                    # print(f"{p2} wins")
                    survival.append(p2)
                elif p1.getTime() == p2.getTime():
                    if random.randint(0,1):
                        # print(f"{p1} wins on random")
                        survival.append(p1)
                    else:
                        # print(f"{p2} wins on random")
                        survival.append(p2)
            # print("After the battles")
            # print(survival)
            # print("\n")
            if len(population):
                survival.extend(population)
            return survival

        def nSelect(survivors,size=lotsize):
            """Selects the surviours based on lot size, it the best of the \n
                survivours that fills the lotsize\n            
            """
            selected=[]
            #Swapping
            for i in range(len(survivors)):
                for  j in range(i+1,len(survivors)):
                    if survivors[i].getTime()>survivors[j].getTime():
                        temp=survivors[i]
                        survivors[i]=survivors[j]
                        survivors[j]=temp
            if len(survivors) <size:
                return survivors
            else:
                for i in range(0,size):
                    selected.append(survivors[i])
                return selected
            

        parentChromosomes=generateRandomChromosomes()
        calculateChromosome(parentChromosomes)
        selected=[]
        generation=0
        if test==False:
            while (generation < gernerationLimit):
                calculateChromosome(parentChromosomes)
                childChromosomes=mutatation(parentChromosomes)
                calculateChromosome(childChromosomes)
                population=mergePopulation(parentChromosomes,childChromosomes)
                survivors=binaryTournamentSelection(population)
                selected=nSelect(survivors)
                parentChromosomes=selected
                generation+=1
            if len(selected)>0:
                broker.assignResourcesChromosome(selected[0])
                printChromosomeTaskId([selected[0]])
                broker.updateSeqPointer(broker.getResourceLength())
                print(selected[0])
            else:
                print("Ga algorithm has no selected chromosome")
        if test==True:
            user_input=input('Give the lot size seperated by commas eg 1,2,3\n')
            lotlist= list(map(lambda x:x.strip(),user_input.split(',')))
            timelister=[]
            for lot in lotlist:
                lotsize=lot
                timestart=time.time()
                while (generation < gernerationLimit):
                    calculateChromosome(parentChromosomes)
                    childChromosomes=mutatation(parentChromosomes)
                    calculateChromosome(childChromosomes)
                    population=mergePopulation(parentChromosomes,childChromosomes)
                    survivors=binaryTournamentSelection(population)
                    selected=nSelect(survivors)
                    parentChromosomes=selected
                    generation+=1
                if len(selected)>0:
                    broker.assignResourcesChromosome(selected[0])
                else:
                    print("Ga algorithm has no selected chromosome")
                timeend=time.time()
                timeduration=timestart-timeend
                timelister.append(timeduration)
            return lotlist,timelister
    
    def getHighestProcessingPower(self,devices:list[DeviceNode]):
        """Gets the highest processing power from the list of the devices"""
        if len(devices)<=0:
            # print(f"Error: TraceBack {__name__}: No list Given")
            return None
        pp=-1
        device_is=None
        for device in devices:
            assert isinstance(device,DeviceNode)
            if device.getProcessingPower()>pp:
                pp=device.getProcessingPower()
                device_is=device
        assert isinstance(device_is,DeviceNode)
        return device_is
            

    def dynamicAlgorithm(self,brokerSleep=5):
        """
        Algorithm initially allocates a task to the first available device(based on the highest processing power available)\n
        When all the devices are occupied , it then checks for the first available device after completing the task.\n
        If free is allocated with another task\n
        """
        print("Allocating using Dynamic Algorithm")
        broker=self.__broker
        assert isinstance(broker,Broker)
        clusterThreads=[]
        clusterParallelobj=[]
        network=self.__network
        assert isinstance(network,Network)
        layer0=network.getNetworkLayers()[0]
        assert isinstance(layer0,Layer)
        clusters=layer0.getClusters()

        self.stopDynamicAlgorithm=False
        def allocate():
            while(not(self.stopDynamicAlgorithm)):
                while(not(broker.isResourceEmpty())):
                    nonactive=[]
                    for cluster in clusters:
                        nonactive.extend(cluster.getNonActiveDevices())
                        deviceis=self.getHighestProcessingPower(nonactive)
                    if not(deviceis ==None):
                        broker.assignLinearResources(deviceis)
                   
                print(f"Broker has no task list , Sleeping for {brokerSleep}")
                time.sleep(brokerSleep)
            
        allocate()



    def getAlgorithm(self):
        """
        Returns the algorithm (the value associated with the class variable such as Algorithm.__RoundRobin)\n
        """
        return self.__algorithm




            
def getTaskleft(cluster):
    """Prints the task left in a device queue of the devices in a  cluster"""
    assert isinstance(cluster,Cluster)
    print("\nGetting Task left info")
    while(True):
        listprint=[]
        for device in cluster.getDevices():
            assert isinstance(device,DeviceNode)
            listprint.append(len(device.getResourceList()))
        if any(listprint):
            print(f"\n{listprint}")
        else:
            print(f"\n{listprint}")
            print("\nStopped getting Task left info")
            break

        time.sleep(0.5)




if __name__=="__main__":
    # network=Network()
    # network.dummyNetwork()
    # layer0=network.getNetworkLayers()[0]
    # tasks=TaskGenerator.generatenoTask(15)
    # cluster=layer0.getClusters()[0]
    # broker=Broker(network)
    # broker.setResourceList(tasks)
    # broker.resourceAllocationAlgorithmStatic(Algorithm._RandomAllocation
    # )
    # clusterPobj=ClusterParallelization(cluster)
    # broker.allDeviceStateSummary()
    # input('Press Enter to start')
    # t1=Thread(target=clusterPobj.clusterParallelization)
    # t2=Thread(target=broker.getDeviceStatusinfo,args=(network,))
    # t1.start()
    # t2.start()
    # t1.join()
    # t2.join()

    network=Network()
    network.dummyNetwork()
    clusterThreads=[]
    clusterParallelobj=[]
    assert isinstance(network,Network)
    layer0=network.getNetworkLayers()[0]
    assert isinstance(layer0,Layer)
    clusters=layer0.getClusters()
    broker=Broker(network)
    tasks=TaskGenerator.generatenoTask(20)
    broker.setResourceList(tasks)
    broker.resourceAllocationAlgorithmStatic(Algorithm._WeightedRoundRobin)
    broker.allDeviceStateSummary()
    input('Press Enter to start')
    #Creating ClusterParallelization object
    for cluster in clusters:
        cluster_Pobj=ClusterParallelization(cluster)
        clusterParallelobj.append(cluster_Pobj)
    #Assigning each clusterParallelization object to a thread, allows each cluster
    #to have concurrent execution
    for cluster in clusterParallelobj:
        assert isinstance(cluster,ClusterParallelization)
        thread=Thread(target=cluster.clusterParallelization)
        clusterThreads.append(thread)
    t1=Thread(target=broker.getDeviceStatusinfo,args=(network,1,True))
    for thread in clusterThreads:
        thread.start()
    t1.start()
    for thread in clusterThreads:
        thread.join()
    t1.join()
    broker.assignLinearResources()



