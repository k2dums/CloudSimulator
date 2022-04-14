#This class tells the requiste for the task that needs to be executed
from typing import Final
class Task:
    TASK_ID=0
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
    def __init__(self,reqDevice,taskName="",instrn_length=0,fileSize=0,outputSize=0) -> None:
        if taskName=="":
            taskName=str(Task.TASK_ID)
        self.id=Task.TASK_ID
        self.__taskName=taskName
        self.__reqDevice:Final=reqDevice
        self.__startTime='NA'
        self.__finshTime='NA'
        self.__duration='NA'
        self.__InstructionLength:Final[int]=instrn_length
        self.__FileSize:Final[int]=fileSize
        self.__OutputSize:Final[int]=outputSize
        self.__status=Task.CREATED
        self.__priority=1
        Task.__updateTask_ID()
        
    
    def __updateTask_ID():
        Task.TASK_ID+=1

    def getInstructionLength(self):
        return self.__InstructionLength
    
    def getId(self):
        return self.id
