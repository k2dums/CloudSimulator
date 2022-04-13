#This is the main py file where everything is abstracted and used

from Network import Network
from Broker import Broker  
from Broker import Algorithm 
from Task import Task
from Graph import Graph
if __name__ == "__main__":
    #instances for the task
    taskA=Task(2,"I am Task 1",2000,200,200)
    taskB=Task(3,"I am Task 2",4000,400,400)
    taskC=Task(1,'',6000,600,600)
    taskD=Task(1,"I am Task 3",8000,800,800)
    taskE=Task(2,"",10000,1000,1000)
    taskF=Task(5,"",12000,1200,1200)
    taskG=Task(2,"I am Task 1",2000,200,200)
    taskH=Task(3,"I am Task 2",4000,400,400)
    taskI=Task(1,'',6000,600,600)
    taskJ=Task(1,"I am Task 3",8000,800,800)
    taskK=Task(2,"",10000,1000,1000)
    taskL=Task(5,"",12000,1200,1200)

    task=[taskA,taskB,taskC,taskD,taskE,taskF,taskG,taskH,taskI,taskJ,taskK,taskL]
    
    algorithms=[Algorithm._RandomAllocation,Algorithm._RoundRobin,Algorithm._WeightedRoundRobin]
    namelist=["Random Allocation","Round-Robin","Weighted Round-Robin"]
    network=Network()
    network.createAndLayerSpecs()
    broker=Broker(network)
    broker.setResourceList(task)
    timeList=[]
    # broker.resourceAllocationAlgorithm(algorithms[1])
    # broker.AllDeviceStateSummary()
    # print(broker.startSimulation())

    for algo in algorithms:
        broker.resetTaskAllocated()
        broker.resourceAllocationAlgorithm(algo)
        time=broker.startSimulation()
        print(time)
        timeList.append(time)
    
    print(timeList)
    Graph.plotBarGraph(namelist,timeList)
  
    print("\n\n")

  


