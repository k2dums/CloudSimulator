import random
import Task

class TaskGenerator:

    def generatenoTask(task_no=10)->list[Task.Task]:
        """
        The function generates number of taks object based on task_no mentioned
        default value for task_no is 10
        The task object generated will be defaultly initialised with instruction length 4000
        """
        tasks=[]
        for i in range(task_no):
            task=Task.Task()
            tasks.append(task)
        return tasks

    def randomTasksgenerator(task_no=10):
        #0 for easy task, 1 for medium task, 2 for large task
        """
        The function generates random task with varied size of task
        Generates the number of task based on number of task_no
        
        """
        tasks=[]
        prob=[0,1,2,0,1,1,0]
        for i in range(task_no):
            random_no=random.randint(0,len(prob)-1)
            random_no=prob(random_no)
            if random_no==0:
                task=Task.smallTask()
            elif random_no==1:
                task=Task.mediumTask()
            elif random_no==2:
                task==Task.mediumTask()
            else:
                print('Error: with creating task in randomTasksgenerator(), creating default task')
                task=Task.Task()
            tasks.append(task)
        return tasks

