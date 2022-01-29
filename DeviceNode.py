from typing import Final

from sympy import memoize_property


class DeviceNode:
    __DEVICEID=1
    CREATED:Final[int]=0
    READY:Final[int]=1
    QUEUED:Final[int]=1
    SUCCESS:Final[int]=4
    FAILED:Final[int]=5
    PAUSED:Final[int]=7
    RESUMED:Final[int]=8
    FAILED_RESOURCE_UNAVAILABLE:Final[int]=9
    def __init__(self,pp=2000,ram=4,memory=500,downloadR=100,uploadR=100,powerWatt=-1) -> None:
        #this id correponds to the device\node 
        self.__deviceId:int=DeviceNode.__setDeviceId()
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
        #whether the device is station or not
    
    
    def __setDeviceId() ->int:
        DeviceNode.__DEVICEID +=1
        return (DeviceNode.__DEVICEID-1)
    
    def setSpecification(self,processingPower=2000,ram=4,memory=500,downloadRate=100,uploadRate=100,powerWatt=-1):
        processingPower=int(input("Give the processing power in MIPs:"))
        if( int(input("Would you like to give more details for the device ,1 for yes else 0:"))==1 ):
            ram=int(input("Give the RAM size in GB:"))
            memory=int(input("Give the Memory space in GB:"))
            downloadRate=int(input("Give the download Rate in Mbps:"))
            uploadRate=int(input("Give the Upload Rate in Mbps:"))
            powerWatt=int(input("Watt usage of the device:"))
        self.__setProcessingPower(processingPower)
        self.__setRam(ram)
        self.__setMemory(memory)
        self.__setDownloadRate(downloadRate)
        self.__setUploadRate(uploadRate)
        self.__setPowerWatt(powerWatt)

        
    def getConfig(self)->None:
        print("Device id =",self.getDeviceId())
        print("Processing Power:",self.getProcessingPower())
        print("Instruction Length:",self.getInstructionLength())
        print("Ram:",self.getRam())
        print("Memory:",self.getMemory())
        print("Download Rate:",self.getDownloadRate())
        print("Upload Rate:",self.getUploadRate())
        print("Resource List:",self.getResourceList())
        print("PowerWatt:",self.getPowerWatt())
    
    def getDeviceId(self):
        return self.__deviceId
    def getProcessingPower(self):
        return self.__processingPower
    def getInstructionLength(self):
        return self.__instructionLength
    def getRam(self):
        return self.__ram
    def getMemory(self):
        return self.__memory
    def getDownloadRate(self):
        return self.__downloadRate
    def getUploadRate(self):
        return self.__uploadRate
    def getExecutionStartTime(self):
        return self.__execStartTime
    def getFinishTime(self):
        return self.__finishTime
    def getResourceList(self):
        return self.__resourceList
    def getPowerWatt(self):
        return self.__powerWatt

   
    def __setProcessingPower(self,pp:int):
        self.__processingPower=pp
    def __setInstructionLength(self,il):
        self.__instructionLength=il
    def __setRam(self,ram:int):
        self.__ram=ram
    def __setMemory(self,m:int):
        self.__memory=m
    def __setDownloadRate(self,dr:int):
        self.__downloadRate=dr
    def __setUploadRate(self,ur:int):
        self.__uploadRate=ur
    def __setExecutionStartTime(self,est):
        self.__execStartTime=est
    def __setFinishTime(self,ft):
        self.__finishTime=ft
    def __setResourceList(self,rl):
        self.__resourceList=rl
    def __setPowerWatt(self,pw:float):
        self.__powerWatt=pw

