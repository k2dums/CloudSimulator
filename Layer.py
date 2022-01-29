#Layer Connection matrix  is used for the connection between clusters 
#The LayerId static variable needs to be part of the Network class
import numpy as np
from DeviceNode import DeviceNode
from Mobile import Mobile
from Station import Station
class Layer:

    def __init__(self,layerId) -> None:
        # self.__clusters=2
        # self.__station=1
        # self.__devicePerCluster=[1,1]
        # self.__connectionMatrix=[[1,1]]
        self.__layerId=layerId
        self.inputData()
    
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

        #Now we need connection ,see if they are connected
        #Here the connection_matrix is simply to find to connection of clsuter to cluster
        # self.__connectionMatrix=np.zeros((self.__clusters,self.__clusters))
        # print("If Connection exist give 1 else 0")
        # for i in range(self.__clusters):
        #     for j in range(self.__clusters):
        #         if i==j:
        #             continue
        #         print(f'Connection between cluster {i} and cluster {j}:')
        #         value=-1
        #         while value!=0 and value!=1 :
        #             value=int(input("Connection value=:"))
        #             if value!=0 and value!=1:
        #                 print("Error with the connection value try again:")
        #         self.__connectionMatrix[i][j]=value
        # self.__devicePerCluster=np.array(self.__devicePerCluster)
        # print(self.__devicePerCluster)


    #Overall DataStructure  for an entity in self.__deviceSpec_inLayer
     # [   [ [device] [station]  ]        ]
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


    #This reuqests from user to set standard specification or set each specifcation
    def specificationRequest(self):
        print("\n")
        print(f"Layer-{self.__layerId} Device Specifications Config")
        print("Would you like to set standard specification or set each specification")
        print("Type 1 for standard specification ,else user will be setting each specfication:")
        if int(input())==1:
            self.__standardSpecification()
        else:
            self.__eachDeviceSpecification()

        
    def printAbstractData(self):
        print("Station:",self.__station)
        print("Clusters",self.__clusters)
        print("Device Per Cluster",self.__devicePerCluster)
        print("Connection Matrix:\n",self.__connectionMatrix)
    
    def printLayerSummary(self):
        print("\n")
        print(f"Layer-{self.__layerId} Summary".center(100," "))
        print(f"Device Id".center(20," ")+"|"+f"Processing Power".center(20," ")+"|"+f"WattUsage".center(20," ")+"|"+f"Battery".center(20," ")+"|"+f"Type".center(20," "))
        # for cluster in enself.__deviceSpec_inLayer:
        #     print("Cluster Value",cluster)
        #     print("cluster",type(cluster))
        #     for device in cluster:
        #         print("Device Value",device)
        #         print("device",type(device))
        #         for obj in device:
        #             print("obj an instance",isinstance(obj,DeviceNode))
        #             break
        #         break
        #     break

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
    
