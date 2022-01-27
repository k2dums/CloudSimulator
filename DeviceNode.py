from typing import Final


class DeviceNode:
    __deviceId=1
    CREATED:Final[int]=0
    READY:Final[int]=1
    QUEUED:Final[int]=1
    SUCCESS:Final[int]=4
    FAILED:Final[int]=5
    PAUSED:Final[int]=7
    RESUMED:Final[int]=8
    FAILED_RESOURCE_UNAVAILABLE:Final[int]=9
    def __init__(self,pp=2000,ram=4,memory=500,downloadR=100,uploadR=100,powerWatt=-1,isStation="Unknown") -> None:
        #this id correponds to the device\node 
        self.__deviceId:int=DeviceNode.setDeviceId()
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
        self.__isStation=isStation
    
    def setDeviceId():
        DeviceNode.__deviceId+=1
        return DeviceNode.__deviceId-1
    
    def setSpecification(self,processingPower=2000,ram=4,memory=500,downloadRate=100,uploadRate=100,powerWatt=-1,prompt:int=-1):
        if prompt !=-1:
            processingPower=int(input("Give the processing power in MIPs:"))
            if( int(input("Would you like to give more details for the device ,1 for yes else 0:"))==1 ):
                ram=int(input("Give the RAM size in GB:"))
                memory=int(input("Give the Memory space in GB:"))
                downloadRate=int(input("Give the download Rate Mbps:"))
                uploadRate=int(input("Give the Upload Rate Mbps:"))
                powerWatt=int(input("Watt usage of the device:"))
        self.__init__(processingPower,ram,memory,downloadRate,uploadRate,powerWatt,False)

        
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
    def getIsStation(self):
        return self.__isStation