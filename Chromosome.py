#Eqivalent to a layer in the network
from Cluster import Cluster
from Task import Task
class Chromosome:
    """
    Class is used for Genetic Algorithm \n
    It has a structure similar to a layer in a network\n
    You can create a Chromosome by passing a network Layer\n
    Or by explicitly using the methods in the class\n
    """
    _id=1
    def __init__(self) -> None:
        self.__id=Chromosome._id
        self.__section=[]
        self.__time=-1
        self.__sectionNo=0
        Chromosome._id+=1
    
    def creationViaLayer(self,layer):
        """Creates the chromosome layer if the layer of a network instance is given"""
        for cluster in (layer.getClusters()):
            assert isinstance(cluster,Cluster)
            self.viaLayercreateSection(cluster.getNoOfDevice())
            self.__sectionNo+=1


    def __str__(self):
        return f'Chromosome {self.__id},Time {self.getTime()}'
    
    def __repr__(self) -> str:
        return f'Chromosome {self.__id},'
        

    def viaLayercreateSection(self,devices):
        """Creates section of a chromosome via layer of the network instance"""
        section=self.Chormosome_section(self.__sectionNo)
        section.createSectionViaLayer(devices)
        self.__section.append(section)
        self.__sectionNo+=1
    
    def createSection(self):
        """Creates the section of a chromosome"""
        section=self.Chormosome_section(self.__sectionNo)
        self.__section.append(section)
        self.__sectionNo+=1
        return section

    def getSections(self):
        """Returns the section of a chromosome"""
        return self.__section
    def getId(self):
        """Returns the id of the chromosome"""
        return self.__id
    def getTime(self):
        """Gets the time taken for the chromsome encoding for processing the task"""
        return self.__time
    def setTime(self,time):
        """Sets the time  taken for the chormosome encoding for processing the task"""
        self.__time=time
    def setId(self,id):
        """Sets the id for the chromosome """
        self.__id=id
  
        


    class Chormosome_section:
        """ An innter class to the Chromosome Class\n
            This is for the chromosome section \n
            Equivalent to a cluster in the network\n
        """
        def __init__(self,id) -> None:
            self.__id=id
            self.__units=[]
            self.__deviceNo=0
       
        def createSectionViaLayer(self,devices):
            """Creates the section from the layer of the netwokr instance"""
            for i in range(devices):
                self.createUnit()

        def getUnits(self):
            """Returns the number of units in the chromosome section """
            return self.__units
        def createUnit(self):
            """Creates the unit in the chormosme section """
            unit=self.Chromosome_unit(self.__deviceNo)
            self.__deviceNo+=1
            self.__units.append(unit)
            return unit
        def getId(self):
            return self.__id
         
        class Chromosome_unit:
            """Inner class to the Chromosome seciton \n
               Equivalent to a device in a network\n    
            """
            def __init__(self,id) -> None:
                self.__id=id
                self.__task=[]
            def setTask(self,task:Task):
                """Sets the task to the unit"""
                self.__task.append(task)
            def getTasks(self)->list[Task]:
                """Gets task from the unit"""
                return self.__task
            def getId(self):
                """returns the id of the chromosome unit"""
                return self.__id
