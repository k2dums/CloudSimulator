
from threading import Thread
from TaskGenerator import TaskGenerator
from Task import Task
from Cluster import Cluster
from DeviceNode import DeviceNode
from Mobile import Mobile
from Station import Station
import time
from Network import Network
import LogFile


class ClusterParallelization:
    """
    Class for allowing parallel Cluster simulation (simulating the processing of task in a device)\n
    The device processing simulation is achieved by threads \n
    If there are 5 devices in the cluster, 5 threads representing 5 devices will be created\n
    This provides concurrent simulation of the devices\n
    It takes cluster object a parameter\n
    """

    id_pointer=0
    def __init__(self,clusterobj) -> None:
        self.id=ClusterParallelization.id_pointer
        self.clusterobj=clusterobj
        self.device_threads=[]
        self.stopParallelization_Flag=False
        ClusterParallelization.id_pointer+=1

    def __repr__(self) -> str:
        return f'Parallelizaiton {self.id}'

    def deviceParallelization(self,deviceobj):
        """
        Function helps to simulate the devices and the task it needs to process simulate\n
        Say the task is 40000 Million instruction , and if the device has processing power\n
        of 4000 MIPS , then the device completes the task in 10 sec, this is simulated by making the\n 
        thread sleep for 10 sec and then processing the task to be completed by updating the resourceList\n 
        of the device\n
        """
     
        assert isinstance(deviceobj,DeviceNode)
        print(f"\n[STARTING] Device {deviceobj.getDeviceId()} Parallelization")
        processingpower=deviceobj.getProcessingPower()
        timeIdle=-1
        while(not(self.stopParallelization_Flag)):
            while(deviceobj.isThereTask()):
                timeIdle=-1
                task=deviceobj.getResourceList()[0]
                assert isinstance(task,Task)
                #time to process in seconds
                timetoprocess=task.getInstructionLength()/processingpower
                #After sleeping the task  is said to be processed and completed
                print(f"\nDevice {deviceobj.getDeviceId()} will take {timetoprocess} seconds to complete task {task.getId()}")
                deviceobj.setStatus(DeviceNode.PROCESSING)
                time.sleep(timetoprocess)
                deviceobj.setStatus(DeviceNode.SUCCESS)
                print(f"\nTask {task.getId()} is compeleted by device {deviceobj.getDeviceId()}")
                tasks=deviceobj.getResourceList()
                #removing the processed task, marking it completed
                if len(tasks)==1:
                    deviceobj.updateResourceList([])
                else:
                    tasks=tasks[1:len(tasks)]
                    deviceobj.updateResourceList(tasks)
            if timeIdle==-1:
                timeIdle=time.perf_counter()
            elif (deviceobj.getStatus()!=DeviceNode.IDLE) and ((time.perf_counter()-timeIdle)>=5):
                deviceobj.setStatus(DeviceNode.IDLE)
            #if no task in the device , check after a while
            time.sleep(0.1)


    def clusterParallelization(self):
        """
        Helps in parallizaion of the cluster where the devices  in the cluster needs\n
        to have concurrent processing simulation\n
        """
    
        self.stopParallelization_Flag=False
        assert isinstance(self.clusterobj,Cluster)
        print(f"\n[STARTING] Cluster Parallelization {self.clusterobj.getId()}")
        cluster=self.clusterobj
        assert isinstance(cluster,Cluster)
        devices=cluster.getDevices()
        for device in devices:
            thread=Thread(target=self.deviceParallelization,args=(device,))
            self.device_threads.append(thread)
        for devicethread in self.device_threads:
            devicethread.start()
        for devicethread in self.device_threads:
            devicethread.join()
        # while (not(self.stopParallelization_Flag)):
        #     time.sleep(0.1)
        print(f"\n[TERMINATED] Cluster Parallelization {self.clusterobj.getId()}")


    def stopParallelization(self):
        self.stopParallelization_Flag=True
    
    def taskCheck(self):
        """
            Return True if task is there in the cluster associated with the clusterParallizaiton object\n
        """
        return self.clusterobj.isThereTask()

