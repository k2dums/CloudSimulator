
from typing import Final

class Task:
    """
    Class is an abstraction for a real world task\n
    This class tells the requiste for the task that needs to be executed\n
    Every task such as email, browsing or other such tasks can inherit this class and create a requiste \n
    for the execution of that task\n
    """
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

    def __init__(self,reqDevice=-1,taskName="",instrn_length=4000,fileSize=0,outputSize=0) -> None:
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
    
    def __str__(self):
        return f'Task-{self.id}'
    
    def __repr__(self) -> str:
        return f'Task-{self.id}'
        
        
    
    def __updateTask_ID():
        Task.TASK_ID+=1

    def getInstructionLength(self):
        """Returns the instruction length of the task"""
        return self.__InstructionLength
    
    def getId(self):
        """Returns the id of the task"""
        return self.id


def smallTask():
    """
    Function returns a task object\n
    The task object has instruction length 4000\n
    """
    task=Task()
    return task

def mediumTask():
    """
    Function returns a task object \n
    The task object has an instruction length of 10,000\n
    """
    task=Task(instrn_length=10000)
    return task
    

def largeTask():
    """
    Function returns a task object\n
    The task object has an instruction length of 40,000\n
    """
    task=Task(instrn_length=40000)
    return task

if __name__=="__main__":
    pass
