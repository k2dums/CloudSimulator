#This class is for allocating the resources and also is reponsible for the schdeduling algorithm used
#It assigns the broker id to the device when allocating the resources to it
from scipy import rand
from sqlalchemy import null
from Cluster import Cluster
from Network import Network
from DeviceNode import DeviceNode
from Mobile import Mobile
from Station import Station
from Layer import Layer
from Task import Task
import random


#Eqivalent to a layer in the network
class Chromosome:
    _id=1
    def __init__(self,layer:Layer) -> None:
        self.__id=Chromosome._id
        self.__section=[]
        self.__time=-1
        for cluster in (layer.getClusters()):
            assert isinstance(cluster,Cluster)
            self.createSection(cluster.getNoOfDevice())
        Chromosome._id+=1

    def createSection(self,devices):
        section=self.Chormosome_section(devices)
        self.__section.append(section)
    def getSections(self):
        return self.__section
    def getId(self):
        return self.__id
    def getTime(self):
        return self.__time
    def setTime(self,time):
        self.__time=time
        

#Equivalent to a cluster in the network
    class Chormosome_section:
        def __init__(self,devices:int) -> None:
            self.__units=[]
            for i in range(devices):
                self.createUnits()
        def getUnits(self):
            return self.__units
        def createUnits(self):
            unit=self.Chromosome_unit()
            self.__units.append(unit)

#Equivalent to a device in a network             
        class Chromosome_unit:
            def __init__(self) -> None:
                self.__task=[]
            def setTask(self,task:Task):
                self.__task.append(task)
            def getTasks(self)->list[Task]:
                return self.__task
class Broker:
    __BROKER_ID=0
    __state=["CREATED","READY","QUEUED","SUCCESS","FAILED","PAUSED","RESUMED","FAILED_RESOURCE_UNAVAILABLE"]

    
    def __init__(self,network) -> None:
        self.__network=network
        self.__brokerId=Broker.__BROKER_ID
        self.__deviceId=0
        self.dynamicAllocation=False
        self.__resourceList=[]
        self.__allocatedTask=[]
        Broker.__BROKER_ID+=1
        assert isinstance(self.__network,Network)

    

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
        self.__allocatedTask.append(self.__resourceList[self.__seq_pointer])
        self.__seq_pointer+=1
    
    def assignResourcesChromosome(self,chromosomeList:list[Chromosome]) ->None:
        #if list is empty return immediately
        if not(chromosomeList):
            return 
        assert isinstance(self.__network,Network)
        for chromosome in chromosomeList:
            for sectionNo,section in enumerate(chromosome.getSections()):
                for unitNo,unit in enumerate(section.getUnits()):
                    if unit.getTask():
                        for task in unit.getTask():
                            self.__network.getNetworkLayers()[0].getClusters[sectionNo].getDevices[unitNo].setResourceList(task)
        # for clusterno,cluster in enumerate(chromosome):
        #     for deviceno,device in enumerate(cluster):
        #         if device ==1:
        #             obj=self.__network.getNetworkLayers()[0].getClusters[clusterno].getDevices[deviceno]
        #             self.assignLinearResources(obj)


    
 
        


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



        


            

    def resourceAllocationAlgorithm (self,algorithm=1):
        self.__algo=Algorithm(self.__network,self)
        self.__algo.resourceAllocation(algorithm)

    def printWeightNetwork(self):
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
    
    # def loadbalancing(self,algorithm):
    #     if not(hasattr(self,"_Broker__algorithm")):
    #         print("Error:No prior allocation of task")
    #         return-
    #     self.__algo.loadbalancing()

    
    def startSimulation(self):
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
        assert isinstance(self.__network,Network)
        self.__network.resetTaskAllocated()
        self.__seq_pointer=0
    def deviceBreakDown(deviceObj):
        pass
    def updateDeviceStatus(deviceObj):
        pass
    def simualationSummary():
        pass
    def getTaskList(self):
        return self.__resourceList
    
    def setRoundRobinPointer(self,device:DeviceNode):
        if hasattr(self,'_Broker__algo'):
            assert isinstance(self.__algo,Algorithm)
            self.__algo.setRoundRobinPointer(device)

  
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
    _RandomAllocation:int=5
    _GA:int=6

    def __init__(self,network,broker) -> None:

        self.__network=network
        assert isinstance(self.__network,Network)
        self.__broker=broker
        assert isinstance(self.__broker,Broker)
        self.__algorithm=-1
        self.__roundRobinPointer=None

    
    def resourceAllocation(self,algorithm=1):

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
        else:
            print('Error:Allocation Algorithm not present')
    
  


    def setRoundRobinPointer(self,device:DeviceNode):
        self.__roundRobinPointer=device


    #Need for a roundrobin pointer that tracks the last device that was set with taskc
    def roundRobin(self):
        print("Allocating using Round Robin")
        network=self.__network
        assert isinstance(network,Network)  
        broker=self.__broker
        assert isinstance(broker,Broker)
        no_Layers=network.getNumberofLayers()
        layers=network.getNetworkLayers()
        layer0=layers[0]
        assert isinstance(layer0,Layer)

        # #Allocating Tasks only if the devices doesnt have any task
        # def assignWhenPointerNone():  
        #     assert isinstance(layer0,Layer)
        #     # Enter if only when the roundRobin is None
        #     if self.__roundRobinPointer is None:
        #         for cluster in layer0.getClusters():
        #             assert isinstance(cluster,Cluster)
        #             for device in cluster.getDevices():
        #                 assert isinstance(device,DeviceNode)
        #                 if device.getStatus()==DeviceNode.CREATED:
        #                     broker.assignLinearResources(device)
        #                     broker.setRoundRobinPointer(device)
        #                 if broker.isResourceEmpty():
        #                     return
        #     return #if roundRobinPointer not None

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
                        if not(isdeviceFound) and  device== self.__roundRobinPointer:
                            isdeviceFound=True
                        if broker.isResourceEmpty():
                            return
                                

                            
        # assignWhenPointerNone()
        assignTask()
            

       






 
        


    
  
    
    def weightedRoundRobin(self):
        print("Allocation using Weighted Round Robin")
        network=self.__network
        broker=self.__broker
        assert isinstance(broker,Broker) and isinstance(network,Network)
        firstLayer=network.getNetworkLayers()[0]
        assert isinstance(firstLayer,Layer)
        clusterList=[]
        for cluster in firstLayer.getClusters():
            clusterList.append(cluster)
        
        #Calculating the processing power per cluster and finding the minimum processing power in a cluster
        def calculateWeight():
            minimum=-1
            for cluster in clusterList:
                assert isinstance(cluster,Cluster)
                processingPower=0
                for device in cluster.getDevices():
                    assert isinstance(device,DeviceNode)
                    processingPower=processingPower+device.getProcessingPower()
                if minimum==-1:
                    minimum=processingPower
                cluster.setWeight(processingPower)

            #We set the weight (processing power /minimum processing power)
            for cluster in clusterList:
                assert isinstance(cluster,Cluster)
                cluster.setWeight(round(cluster.getWeight()/minimum))

        def sortingClusterbyWeight():
        #Sorting of cluster based on cluster weight
            for i in range(len(clusterList)):
                for j in range(i+1,len(clusterList)):
                    if clusterList[i].getWeight()<clusterList[j].getWeight():
                        temp=clusterList[i]
                        clusterList[i]=clusterList[j]
                        clusterList[j]=temp
                    if clusterList[i].getWeight()==clusterList[j].getWeight():
                        if clusterList[i].getId()<clusterList[j].getId():
                            temp=clusterList[i]
                            clusterList[i]=clusterList[j]
                            clusterList[j]=temp

                
            

        def assignTask():
        #Assigning of task based on weight
            while( not(broker.isResourceEmpty())):
                for cluster in clusterList:
                    assert isinstance(cluster,Cluster)
                    devices=cluster.getDevices()
                    
                    i=0 #This reponsible for the loop (giving the weightage for the cluster)
                    j=0 #This is responsible for the devices in the cluster tracking
                    while (i < cluster.getWeight() ):
                        broker.assignLinearResources(devices[j])
                        j+=1
                        i+=1
                        if not(j<len(devices)):
                            j=0
        calculateWeight()
        sortingClusterbyWeight()
        assignTask()



    
    def randomAllocation(self):
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
    
    def ga(self,no_OfGenerations:int=20):
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
        


        def generateRandomChromosomes(no=10):
            print("Generating pool of random Chromosome")
            chromosomeList=[]
            #Chromosome is network equivalent,section is cluster equivalent,unit is device equivalent
            for i in range(no):
                chromosome=Chromosome(layer)
                for task in broker.getTaskList():
                    randomSection=random.randint(0,len(chromosome.getSections())-1)
                    randomSection=chromosome.getSections()[randomSection]
                    randomUnit=random.randint(0,len(randomSection.getUnits())-1)
                    randomUnit=randomSection.getUnits()[randomUnit]
                    randomUnit.setTask(task)
                chromosomeList.append(chromosome)
            return chromosomeList
        
       


        def calculateChromosome(chromosomeList):
            network=Network()
            broker=Broker(network)
            for chromosome in chromosomeList:
                assert isinstance(chromosome,Chromosome)
                broker.resetTaskAllocated()
                broker.assignResourcesChromosome(chromosome)
                time=broker.startSimulation()
                chromosome.setTime(time)

                



        

        
        def mutatation(chromosomes)->list[list[int]]:
            
            def crossover():
                print("Undergoing crossover of the Chromosome")
                crossoverRange=5
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

                print("Crossover Complete")


            def mutate():
                print("Undergoing mutation of the Chromosome")
                mutateRange=4
                for chromosome in chromosomes:
                    assert isinstance(chromosome,Chromosome)
                    for i in range(mutateRange):
                        #Possibilty of deleting a task or not
                        flag=random.randint(0,1)
                        if flag:
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
                print('Mutation complete')
    
            mutate()
            crossover()







        
        def binaryTournamentSelection():
            pass
            

        

        chromosomes=generateRandomChromosomes()
        printChromosomeCounter(chromosomes)
        mutatation(chromosomes)
        printChromosomeCounter(chromosomes)













        
    
    def getAlgorithm(self):
        return self.__algorithm


            


