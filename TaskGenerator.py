from Task import Task

class TaskGenerator:

    def generatenoTask(task_No=10)->list[Task]:
        tasks=[]
        for i in range(task_No):
            task=Task()
            tasks.append(task)
        return tasks