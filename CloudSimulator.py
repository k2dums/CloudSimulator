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
    algorithms=[Algorithm._RandomAllocation,Algorithm._GA,Algorithm._RoundRobin,Algorithm._WeightedRoundRobin]
    namelist=["Random Allocation","Genetic Algorithm","Round-Robin","Weighted Round-Robin"]
    taskSize=[200, 400, 600, 800, 1000, 1200]
    network=Network()
    network.dummyNetwork()
    broker=Broker(network)
    # broker.setResourceList(task)
    timeList=[]

    for algo in algorithms:
        timealgo=[]
        for size in taskSize:
            tasks=TaskGenerator.generatenoTask(size)
            broker.setResourceList(tasks)
            broker.resetTaskAllocated()
            broker.resourceAllocationAlgorithm(algo)
            time=broker.startSimulation()
            timealgo.append(time)
            if algo==Algorithm._WeightedRoundRobin:
                # broker.ActiveDeviceStateSummary()
                broker.printWeightNetwork()
        timeList.append(timealgo)
    
    Graph.lineGraph(namelist,taskSize,timeList)
    barplotx=[timeTaken[-1] for timeTaken in timeList]
    Graph.plotBarGraph(barplotx,namelist)
    print(timeList)
    # broker.AllDeviceStateSummary()
    print("\n\n")


  

