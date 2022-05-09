#Eqivalent to a layer in the network
from Cluster import Cluster
from Task import Task
class Chromosome:
    _id=1
    def __init__(self) -> None:
        self.__id=Chromosome._id
        self.__section=[]
        self.__time=-1
        self.__sectionNo=0
        Chromosome._id+=1
    
    def creationViaLayer(self,layer):
        for cluster in (layer.getClusters()):
            assert isinstance(cluster,Cluster)
            self.viaLayercreateSection(cluster.getNoOfDevice())
            self.__sectionNo+=1


    def __str__(self):
        return f'Chromosome {self.__id},Time {self.getTime()}'
    
    def __repr__(self) -> str:
        return f'Chromosome {self.__id}'
        

    def viaLayercreateSection(self,devices):
        section=self.Chormosome_section(self.__sectionNo)
        section.createSectionViaLayer(devices)
        self.__section.append(section)
        self.__sectionNo+=1
    
    def createSection(self):
        section=self.Chormosome_section(self.__sectionNo)
        self.__section.append(section)
        self.__sectionNo+=1
        return section

    def getSections(self):
        return self.__section
    def getId(self):
        return self.__id
    def getTime(self):
        return self.__time
    def setTime(self,time):
        self.__time=time
    def setId(self,id):
        self.__id=id
  
        

#Equivalent to a cluster in the network
    class Chormosome_section:
        def __init__(self,id) -> None:
            self.__id=id
            self.__units=[]
            self.__deviceNo=0
       
        def createSectionViaLayer(self,devices):
            for i in range(devices):
                self.createUnit()

        def getUnits(self):
            return self.__units
        def createUnit(self):
            unit=self.Chromosome_unit(self.__deviceNo)
            self.__deviceNo+=1
            self.__units.append(unit)
            return unit
        def getId(self):
            return self.__id
#Equivalent to a device in a network             
        class Chromosome_unit:
            def __init__(self,id) -> None:
                self.__id=id
                self.__task=[]
            def setTask(self,task:Task):
                self.__task.append(task)
            def getTasks(self)->list[Task]:
                return self.__task
            def getId(self):
                return self.__id
