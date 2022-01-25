
from typing import Final
class Cloudlet:
    #This class is bascially for the data centers and various parameters associated with it
    #The parameters ommited in this class are battery-life
    #Parameters for Cloudlet
    CREATED:Final[int]=0
    READY:Final[int]=1
    QUEUED:Final[int]=2
    INEXEX:Final[int]=3
    SUCCESS:Final[int]=4
    FAILED:Final[int]=5
    CANCELED:Final[int]=6
    PAUSED:Final[int]=7
    RESUMED:Final[int]=8
    FAILED_RESOURCE_UNAVAILABLE:Final[int]=9
    

    def __init__(self) -> None:
        self.__cloudletId:Final[int]
        self.__userId:int
        self.__cloudletLength:Final[int] #the length of the instructions
        self.__cloudLetFileSize:Final[int]
        self.__cloudletOutputSize:Final[int]
        self.__status:Final[int]
        self.__execStartTime:float
        self.__finishTime:float
        self.__reservationid:int
        self.__record:Final[bool]
        self.__newline:str
        self.__history:str
        self.__resList:Final[list]
        self.__index:int
        self.__classType:int
        self.__netToS:int
        self.__num
        self.vmId:int
        self.costPerBw:float
        self.accumulatedBwCost:float
        self.utilizationModelCpu
        self.utliziationModelRam
        self.utilizationModelBw
        self.requiredFiles