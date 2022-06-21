from http.client import PROCESSING
from typing import Final
class DeviceNode:
    """
    This class is modelled to abstract a real world device\n
    It contains attributes of a device such as processingPower,ram, bandwidth etc\n 
    """
    __DEVICEID=0
    CREATED:Final[int]=0
    READY:Final[int]=1
    QUEUED:Final[int]=1
    SUCCESS:Final[int]=4
    FAILED:Final[int]=5
    PAUSED:Final[int]=7
    RESUMED:Final[int]=8
    IDLE:Final[int]=9
    PROCESSING:Final[int]=10
    FAILED_RESOURCE_UNAVAILABLE:Final[int]=9
    def __init__(self,pp=4000,ram=4,memory=500,downloadR=100,uploadR=100,powerWatt=-1) -> None:
        #this id correponds to the device\node 
        self.__deviceId:int=DeviceNode.__classSetDeviceId()
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
        #the status of the device
        self.__status:int=DeviceNode.CREATED
        #Need for the number of processors 
        #self.__processors:int=processors
        #Tracks the task that has been finished
        self.__finishList=[]
        self.__idleTime:int=0
    
    def __str__(self) -> str:
        return f'Device {self.__deviceId}'
    def __repr__(self) -> str:
        return f'Device {self.__deviceId}'

    def __classSetDeviceId() ->int:
        """
        This sets the device id for the devices, which can help to identify the device uniquely
        """
        DeviceNode.__DEVICEID +=1
        return (DeviceNode.__DEVICEID-1)
    

    def setSpecification(self,processingPower=2000,ram=4,memory=500,downloadRate=100,uploadRate=100,powerWatt=-1):
        """
            This puts in the device specification such as processing power, ram, memory ,bandwidth etc
        """
        processingPower=int(input("Give the processing power in MIPs:"))
        user=input("Would you like to give more details for the device ,'y' for yes else 'n': ").lower()
        while user !='y' and user !='n':
            print("Error:Invalid User Input")
            user=input("Would you like to give more details for the device ,'y' for yes else 'n': ").lower()
        if( user =='y' ):
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
        """
        Was used for debugging for the class to print the device specification set
        """
        print("Device id =",self.getDeviceId())
        print("Processing Power:",self.getProcessingPower())
        print("Instruction Length:",self.getInstructionLength())
        print("Ram:",self.getRam())
        print("Memory:",self.getMemory())
        print("Download Rate:",self.getDownloadRate())
        print("Upload Rate:",self.getUploadRate())
        print("Resource List:",self.getResourceList())
        print("PowerWatt:",self.getPowerWatt())
    


    #This are the setters and getters for the  respective attribute of the instance of the class
    def getDeviceId(self):
        """Returns the device id"""
        return self.__deviceId
    def getProcessingPower(self):
        """Retunrs the processing power of the device"""
        return self.__processingPower
    def getInstructionLength(self):
        """Returns the instruciton length of the device"""
        return self.__instructionLength
    def getRam(self):
        """Returns the Ram of the device"""
        return self.__ram
    def getMemory(self):
        """Returns the memory of the device"""
        return self.__memory
    def getDownloadRate(self):
        """Returns the download Rate of the device"""
        return self.__downloadRate
    def getUploadRate(self):
        """Returns the upload rate of the device"""
        return self.__uploadRate
    def getExecutionStartTime(self):
        """Returns the exection start time of the device"""
        return self.__execStartTime
    def getFinishTime(self):
        """Returns the finish time of the device"""
        return self.__finishTime
    def getResourceList(self)->list:
        """Returns the resource list of the device"""
        return self.__resourceList
    def getPowerWatt(self):
        """Returns the power Watt of the device"""
        return self.__powerWatt
    def getStatus(self):
        """Returns ths status of the device"""
        return self.__status
    def getStatusText(self):
        """Returns teh satus of the devcice in text (str)"""
        if self.__status==DeviceNode.CREATED:
            return "CREATED"
        elif self.__status==DeviceNode.READY:
            return "READY"
        elif self.__status==DeviceNode.QUEUED:
            return "QUEUED"
        elif self.__status==DeviceNode.SUCCESS:
            return "SUCCESS"
        elif self.__status==DeviceNode.FAILED:
            return "FAILED"
        elif self.__status==DeviceNode.PAUSED:
            return "PAUSED"
        elif self.__status==DeviceNode.RESUMED:
            return "RESUMED"
        elif self.__status==DeviceNode.IDLE:
            return "IDLE"
        elif self.__status==DeviceNode.PROCESSING:
            return "PROCESSING"
        elif self.__status==DeviceNode.FAILED_RESOURCE_UNAVAILABLE:
            return "FAILED RESOURCE UNAVAILABLE"
        else:
            return "NA"

    def __setProcessingPower(self,pp:int):
        """Sets the processing power of the device"""
        self.__processingPower=pp
    def __setInstructionLength(self,il):
        """Sets teh instruction length of the device"""
        self.__instructionLength=il
    def __setRam(self,ram:int):
        """Sets teh ram of the device"""
        self.__ram=ram
    def __setMemory(self,m:int):
        """Sets the memory of the device"""
        self.__memory=m
    def __setDownloadRate(self,dr:int):
        """Sets the download rate of the device"""
        self.__downloadRate=dr
    def __setUploadRate(self,ur:int):
        """Sets the upload rate of the device"""
        self.__uploadRate=ur
    def __setExecutionStartTime(self,est):
        """Sets teh execution start time of the device"""
        self.__execStartTime=est
    def __setFinishTime(self,ft):
        """Sets the finish time of the device"""
        self.__finishTime=ft
    def setResourceList(self,rl):
        """
        This appends the task to the device's resourcelist\n
        """
        self.__resourceList.append(rl)
        self.setStatus(DeviceNode.READY)
    def updateResourceList(self,tasks):
        """
        This directly updates the list of resources (task) in a device\n
        While setResourceList() appends the task to the device resourceList\n
        """
        self.__resourceList=tasks
        # if len(self.__resourceList)<=0:
        #     self.setStatus(DeviceNode.CREATED)
    def __setPowerWatt(self,pw:float):
        """Sets the power watt of the device"""
        self.__powerWatt=pw
    def __setDeviceId(self,id):
        """Sets the device id of the deivce"""
        self.__deviceId=id
    def setStatus(self,status):
        """Sets teh status of the device"""
        self.__status=status
    def resetTask(self):
        """Sets the task of the device"""
        self.__resourceList=[]
        self.setStatus(DeviceNode.CREATED)
    def isThereTask(self):
        """Returns true if there is a tak in the device\n
          else returns false
        """
        if len(self.__resourceList)>0:
            return True
        return False
    def setIdleTimet(self,time):
        """Sets the  time for how long the device was idle """
        self.__idleTime=time
    def appendIdleTime(self,time):
        """Appends the idle time , adds to it of the device"""
        self.__idleTime+=time
    def getIdleTime(self,time):
        """Returns the idle time for the device"""
        return self.__idleTime



if __name__=='__main__':
    print(dir())