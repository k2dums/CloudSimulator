from typing import Final


class DeviceNode:
    CREATED:Final[int]=0
    READY:Final[int]=1
    QUEUED:Final[int]=1
    SUCCESS:Final[int]=4
    FAILED:Final[int]=5
    PAUSED:Final[int]=7
    RESUMED:Final[int]=8
    FAILED_RESOURCE_UNAVAILABLE:Final[int]=9
    def __init__(self,idIs,pp,ram,memory,downloadR,uploadR,powerWatt) -> None:
        #this id correponds to the device\node 
        self.__deviceId:int=idIs
        #Milion intructions per sec
        self.__processingPower:int=pp
        #the length in Million instruction
        self.__instructionLength:int=-1
        #the ram memory available for the node
        self.__ram:int=ram
        #the memory space available for the node
        self.__memory:int=memory
        #the download rate
        self.__downloadRate:float=downloadR
        #the upload rate
        self.__uploadRate:float=uploadR
        #the start time of the node
        self.__execStartTime:float=-1.0
        #the finish time of the node
        self.__finishTime:float=-1.0
        #the resource list 
        self.__resourceList:list=[]
        #the usage of the device
        self.__powerWatt:int=powerWatt
        
    def getConfig(self)->None:
        print("Device id =",self.__deviceId)
        print("Processing Power:",self.__processingPower)
        print("Instruction Length:",self.__instructionLength)
        print("Ram:",self.__ram)
        print("Memory:",self.__memory)
        print("Download Rate:",self.__downloadRate)
        print("Upload Rate:",self.__uploadRate)
        print("Resource List:",self.__resourceList)
        print("PowerWatt:",self.__powerWatt)
    