#This is the main py file where everything is abstracted and used

from Network import Network
from Broker import Broker  
from Broker import Algorithm 
from Task import Task
from Graph import Graph
from TaskGenerator import TaskGenerator
def main():
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
    algorithms=[Algorithm._RandomAllocation,Algorithm._RoundRobin,Algorithm._WeightedRoundRobin]
    namelist=["Random Allocation","Round-Robin","Weighted Round-Robin"]
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


    taskA=Task(2,"I am Task 1",2000,200,200)
    taskB=Task(3,"I am Task 2",4000,400,400)
    taskC=Task(1,'',3000,600,600)
    taskD=Task(1,"I am Task 3",4000,800,800)
    taskE=Task(2,"",5000,1000,1000)
    taskF=Task(5,"",6000,1200,1200)
    taskG=Task(2,"",7000,1000,1000)
    taskH=Task(5,"",8000,1200,1200)
    taskI=Task(2,"",9000,1000,1000)
    taskJ=Task(5,"",10000,1200,1200)
    taskK=Task(2,"",11000,1000,1000)
    taskL=Task(5,"",12000,1200,1200)
    taskM=Task(2,"",13000,1000,1000)
    taskN=Task(5,"",14000,1200,1200)
    taskO=Task(2,"",15000,1000,1000)
    taskP=Task(5,"",16000,1200,1200)
    taskQ=Task(2,"",17000,1000,1000)
    taskR=Task(5,"",18000,1200,1200)
    taskS=Task(2,"",19000,1000,1000)
    taskT=Task(5,"",20000,1200,1200)
    tasks=[taskA,taskB,taskC,taskD,taskE,taskF,taskG,taskH,taskI,taskJ,taskK,taskL,taskM,taskN,taskO,taskP,taskQ,taskR,taskS,taskT]

    # for algo in algorithms:
    #     timealgo=[]
    #     for i in range(50):
    #         broker.setResourceList(tasks)
    #         broker.resetTaskAllocated()
    #         broker.resourceAllocationAlgorithm(algo)
    #         time=broker.startSimulation()
    #         timealgo.append(time)
    #         # if algo==Algorithm._WeightedRoundRobin:
    #         #     broker.ActiveDeviceStateSummary()
    #         #     broker.printWeightNetwork()
    #     timeList.append(timealgo)
    # broker.AllDeviceStateSummary()
    # Graph.lineGraph(namelist,range(50),timeList)

    # # print(timeList)
    # print("\n\n")

  


