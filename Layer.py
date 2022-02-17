#Layer Connection matrix  is used for the connection between clusters 
#The LayerId static variable needs to be part of the Network class
import numpy as np
from DeviceNode import DeviceNode
from Mobile import Mobile
from Station import Station
class Layer:

    def __init__(self,layerId) -> None:
        self.__clusters=2
        self.__devicePerCluster=[[2,2],[2,1]]
        # self.__connectionMatrix=[[0,1],[1,0]]
        self.__layerId=layerId
        self.inputData()
    
    #This is  for  getting  inital input for the number of cluster,devices and stations
    def inputData(self):
        print("\n")
        print(f"Layer-{self.__layerId} Config")
        self.__clusters=int(input("Give the number of Clusters:"))
        self.__devicePerCluster=[]
        #Here we are allocating devices  and stations per cluster
        for i in range(self.__clusters):
            devices=int(input(f"For Cluster {i} give the number of devices:"))
            stations=int(input(f"For Cluster {i} give the number of stations:"))
            self.__devicePerCluster.append([devices,stations])
        self.__devicePerCluster=np.array(self.__devicePerCluster)

    #This is sets the connection for the clusters within a particular layer
    def makeClusterConnection(self):
        #Now we need connection ,see if they are connected
        #Here the connection_matrix is simply to find to connection of clsuter to cluster
        self.__connectionMatrix=np.zeros((self.__clusters,self.__clusters))
        print("If Connection exist give 1 else 0")
        for i in range(self.__clusters):
            for j in range(i+1):
                if i==j:
                    continue
                else:
                    self.__connectionMatrix[i][j]=-1
            for j in range(i+1,self.__clusters):
                print(f'Connection between cluster {i} and cluster {j}:')
                value=-1
                while value!=0 and value!=1 :
                    value=int(input("Connection value=:"))
                    if value!=0 and value!=1:
                        print("Error with the connection value try again:")
            self.__connectionMatrix[i][j]=value
 


    #This is setting the specification for mobile,station,device etc
    def __eachDeviceSpecification(self):
        #This is a list containing the devices specifications for each cluster
        self.__deviceSpec_inLayer=[]
    
        #if prompt=1 it tells to display and no input the device specification
        #else when prompt!=1 no prmopt and no input for the device specification
        for cluster in self.__devicePerCluster:
            #This if for the normal devices(setting specification)
            specEachDevice=[]
            specEachStation=[]
            for i in  range(int(cluster[0])): #cluster0 represents the deivces
                if input("Is the device mobile or not.Give 1 for yes,else 0") ==1:
                    obj=Mobile()
                    obj.setSpecification()
                    specEachDevice.append(obj)
                else:
                    obj=DeviceNode()
                    obj.setSpecification()
                    specEachDevice.append(obj)

            #This is for the station(setting specfication)
            for i in range(int(cluster[1])):#cluster1 represnts the stations
                obj=Station()
                obj.setSpecification()
                specEachDevice.append(obj)
            specEachCluster=[specEachDevice,specEachStation]
            self.__deviceSpec_inLayer.append(specEachCluster)


      
    #This sets the standard specification for the object created of DeviceNode class
    #We will add standard specification for the devices and station
    #More info can be seen from eachDeviceSpecification()
    #All the devices here are assumed to be non-mobile
    def __standardSpecification(self):
        self.__deviceSpec_inLayer=[]
        for cluster in self.__devicePerCluster:
            specEachDevice=[]
            specEachStation=[]
            for devices in range(cluster[0]):#devices
                    obj=DeviceNode()
                    specEachDevice.append(obj)
            for stations in range(cluster[1]):#stations
                    obj=Station()
                    specEachStation.append(obj)
            specEachCluster=[specEachDevice,specEachStation]
            self.__deviceSpec_inLayer.append(specEachCluster)


    #This requests from user to set standard specification or set each specifcation
    def specificationRequest(self):
        print("\n")
        print(f"Layer-{self.__layerId} Device Specifications Config")
        print("Would you like to set standard specification or set each specification")
        print("Type 1 for standard specification ,else 0 and user will be setting each specfication:")

        userInput=-1
        while (not(userInput==1) and not(userInput==0)):
            userInput=int(input())
            if(not(userInput==1) and not(userInput==0)):
                print("Give valid value")
        if userInput==1:
            self.__standardSpecification()
        elif userInput==0:
            self.__eachDeviceSpecification()

    #Was used for debugging to print the layer charactersitics
    def printAbstractData(self):
        print("Station:",self.__station)
        print("Clusters",self.__clusters)
        print("Device Per Cluster",self.__devicePerCluster)
        print("Connection Matrix:\n",self.__connectionMatrix)
    
    #Prints the summary details of all the device in a particular layer
    def printLayerSummary(self):
        print("\n")
        print(f"Layer-{self.__layerId} Summary".center(100," "))
        print(f"Device Id".center(20," ")+"|"+f"Processing Power".center(20," ")+"|"+f"WattUsage".center(20," ")+"|"+f"Battery".center(20," ")+"|"+f"Type".center(20," "))
        for clusterno,cluster in enumerate(self.__deviceSpec_inLayer):
            print(f"Cluster-{clusterno}".center(75," "))
            for devices in cluster:
                for obj in devices:
                    id:str=f'{obj.getDeviceId()}'.center(20," ")
                    pp:str=f'{obj.getProcessingPower()}'.center(20," ")
                    watt:str=f'{obj.getPowerWatt()}'.center(20," ")
                    if isinstance(obj,Mobile):
                        battery=f'{obj.getBatteryCapcity()}'.center(20," ")
                        type="Mobile"
                    else:
                        battery="None".center(20," ")
                        if isinstance(obj,Station):
                            type="Station"
                        elif isinstance(obj,DeviceNode):
                            type="Non Mobile"
                    type=type.center(20," ")
                    print(f"{id}|{pp}|{watt}|{battery}|{type}")
            




    #The setter and getter for the attributes of the Layer class
    def getCluster(self):
        return self.__clusters

    def getStation(self):
        return self.__station

    def getDevicePerCluster(self):
        return self.__devicePerCluster

    def getConnectionMatrix(self):
        return self.__connectionMatrix

    def setCluster(self,value):
        value=int(value)
        self.__clusters=value

    def setStation(self,value):
        value=int(value)
        self.__station=value

    def setDevicePerCluster(self,valueList):
        #Need to  check the size of the list say if the cluster =3 but list size=4
        if(len(valueList)!=self.__clusters):
            return 
        self.__devicePerCluster=valueList

    def setConnectionMatrix(self,valueMatrix):
        #Need to check the shape of matrix if station and cluster =2,3 but valueMatrix shape=3,3
        self.__connectionMatrix=valueMatrix
    def getdeviceSpec_inLayer(self):
        return self.__deviceSpec_inLayer
    
    def getLayerid(self):
        return self.__layerId
