#This is the main py file where everything is abstracted and used

from Network import Network
from Broker import Broker,Algorithm
from Task import Task
from Graph import Graph
from TaskGenerator import TaskGenerator
if __name__ == "__main__":
    #instances for the task
    # taskA=Task(2,"I am Task 1",2000,200,200)
    # taskB=Task(3,"I am Task 2",4000,400,400)
    # taskC=Task(1,'',6000,600,600)
    # taskD=Task(1,"I am Task 3",8000,800,800)
    # taskE=Task(2,"",10000,1000,1000)
    # taskF=Task(5,"",12000,1200,1200)
    # taskG=Task(2,"I am Task 1",2000,200,200)
    # taskH=Task(3,"I am Task 2",4000,400,400)
    # taskI=Task(1,'',6000,600,600)
    # taskJ=Task(1,"I am Task 3",8000,800,800)
    # taskK=Task(2,"",10000,1000,1000)
    # taskL=Task(5,"",12000,1200,1200)
    #parameters
    #task size
    #network config
    # task=[taskA,taskB,taskC,taskD,taskE,taskF,taskG,taskH,taskI,taskJ,taskK,taskL]
    algorithms=[Algorithm._WeightedRoundRobin,Algorithm._RoundRobin,Algorithm._RandomAllocation,Algorithm._GA]
    namelist=["Weighted Round-Robin","Round-Robin","Random Allocation","Genetic Algorithm",]
    taskSize=[100,200,300,400,500,600]
    network=Network()
    network.dummyNetwork()
    # network.createAndLayerSpecs()
    broker=Broker(network)
    # broker.setResourceList(task)
    timeList=[]

    for algo in algorithms:
        timealgo=[]
        for size in taskSize:
            tasks=TaskGenerator.generatenoTask(size)
            broker.setResourceList(tasks)
            broker.resetTaskAllocated()
            broker.resourceAllocationAlgorithmStatic(algo)
            time=broker.startStaticSimulation()
            timealgo.append(time)
        timeList.append(timealgo)
    
    # broker.allDeviceStateSummary()
    clusters=network.getNetworkLayers()[0]
    clusters=clusters.getClusters()
    # for cluster in clusters:
    #     print(cluster.getActiveDeviceNo())
    
    Graph.lineGraph(namelist,taskSize,timeList)
    # barplotx=[timeTaken[-1] for timeTaken in timeList]
    # Graph.plotBarGraph(values=barplotx,names=namelist)
    print(timeList)
    # broker.AllDeviceStateSummary()
    print("\n\n")


  

