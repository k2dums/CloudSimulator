#This class tells the requiste for the task that needs to be executed
class Task:
    TASK_ID=0
    CREATED=0
    READY=1
    QUEUED=2
    INEXEX=3
    SUCCESS=4
    FAILED=5
    CANCELED=6
    PAUSED=7
    RESUMED=8
    FAILED_RESOURCE_UNAVAILABLE=9

    def __init__(self,reqDevice=-1,taskName="",instrn_length=4000,fileSize=0,outputSize=0)  :
        if taskName=="":
            taskName=str(Task.TASK_ID)
        self.id=Task.TASK_ID
        self.__taskName=taskName
        self.__reqDevice=reqDevice
        self.__startTime='NA'
        self.__finshTime='NA'
        self.__duration='NA'
        self.__InstructionLength=instrn_length
        self.__FileSize=fileSize
        self.__OutputSize=outputSize
        self.__status=Task.CREATED
        self.__priority=1
        Task.__updateTask_ID()
    
    def __str__(self):
        return f'Task-{self.id}'
    
    def __repr__(self)  :
        return f'Task-{self.id}'
        
        
    
    def __updateTask_ID():
        Task.TASK_ID+=1

    def getInstructionLength(self):
        return self.__InstructionLength
    
    def getId(self):
        return self.id
