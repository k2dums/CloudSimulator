import random
import Task

class TaskGenerator:
    """
    A class used to generate task for the simulation\n
    """

    def generatenoTask(task_no=10)->list[Task.Task]:
        """
        The function generates number of taks object based on task_no mentioned\n
        default value for task_no is 10\n
        The task object generated will be defaultly initialised with instruction length 4000\n
        """
        tasks=[]
        for i in range(task_no):
            task=Task.Task()
            tasks.append(task)
        return tasks

    def randomTasksgenerator(task_no=10):
        #0 for easy task, 1 for medium task, 2 for large task
        """
        The function generates random task with varied size of task\n
        Generates the number of task based on number of task_no\n
        
        """
        tasks=[]
        prob=[0,1,2,2,2,1,1]
        for i in range(task_no):
            random_no=random.randint(0,len(prob)-1)
            random_no=prob[random_no]
            if random_no==0:
                task=Task.smallTask()
            elif random_no==1:
                task=Task.mediumTask()
            elif random_no==2:
                task=Task.largeTask()
            else:
                print('Error: with creating task in randomTasksgenerator(), creating default task')
                task=Task.Task()
            tasks.append(task)
        return tasks

if __name__=="__main__":
    tasks=TaskGenerator.randomTasksgenerator()
    for task in tasks:
        print(task)
