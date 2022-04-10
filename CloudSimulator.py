#This is the main py file where everything is abstracted and used

from Network import Network
from Broker import Broker  
from Broker import Algorithm 
from Task import Task
if __name__ == "__main__":
    #instances for the task
    taskA=Task(2,"I am Task 1",200,200,200)
    taskB=Task(3,"I am Task 2",400,400,400)
    taskC=Task(1,"I am Task 3",800,800,800)
    taskD=Task(1,'',600,600,600)
    taskE=Task(2,"",1000,1000,1000)
    taskF=Task(5,"",1200,1200,1200)

    task=[taskA,taskB,taskC,taskD,taskE,taskF]
    
    network=Network()
    network.createAndLayerSpecs()
    broker=Broker(network)
    broker.setResourceList(task)
    broker.resourceAllocationAlgorithm(Algorithm._WeightedRoundRobin)
    broker.AllDeviceStateSummary()
    broker.printWeightNetwork()
    broker.printUtilizationPerLayerPerCluster()
    
    print("\n\n")

  


