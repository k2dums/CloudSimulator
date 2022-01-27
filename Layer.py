#GraphData not suitable name and needs to be changed
#Can be seen as a a layer and the clusters in that Layer
#Naming can be Layer.py
#Connection matrix can be removed since the connection will be handled by the network.py
import numpy as np
from Mobile import Mobile
from DeviceNode import DeviceNode
class Layer:
    __LAYER_ID=0
    def __init__(self) -> None:
        # self.__clusters=2
        # self.__station=1
        # self.__devicePerCluster=[1,1]
        # self.__connectionMatrix=[[1,1]]
        self.__layerId=Layer.__LAYER_ID
        Layer.__LAYER_ID+=1
        self.inputData()
    
    def inputData(self):
        print("\n")
        print(f"Layer-{self.__layerId} Config")
        self.__clusters=int(input("Give the number of Clusters:"))
        self.__station=int(input("Give the number of stations:"))
        self.__devicePerCluster=np.array([])
        #Here we are allocating devices per cluster
        for i in range(self.__clusters):
            devices=int(input(f"For Cluster {i} give the number of devices:"))
            self.__devicePerCluster=np.append(self.__devicePerCluster,devices)
        #Now we need connection ,see if they are connected
        #By default a cluster cannot connect directly to another cluster
        #Here the connection_matrix is simply to find to connection of station to cluster
        self.__connectionMatrix=np.zeros((self.__station,self.__clusters))
        print("If Connection exist give 1 else 0")
        for i in range(self.__station):
            for j in range(self.__clusters):
                print(f'Connection between station {i} and cluster {j}:')
                value=-1
                while value!=0 and value!=1 :
                    value=int(input("Connection value=:"))
                    if value!=0 and value!=1:
                        print("Error with the connection value try again:")
                self.__connectionMatrix[i][j]=value

    def __eachDeviceSpecification(self):
        #This is a list containing the devices specifications for each cluster
        #Here we pass in either mobile object or DeviceNode object
        self.__deviceSpec_inLayer=[]
        #This keeps a track of the devices in each cluster
         # clusterDeviceInfo=[   [cluster1]   ,[cluster2] .....[clustern]]
        #if this is cluster1 inside clusterDeviceInfo Then cluster1= [device1_spec,device2_spec,device3_spec]
        #Overall DataStructure  for a cluster entity
         # [   [[],[],[]]     ]
        
        #Below  for when in a cluster there can be a station and devices
        # for cluster in self.__devicePerCluster:
        #     #This if for the normal devices(setting specification)
        #     specEachDevice=[]
        #     specEachStation=[]
        #     for i in  range(int(cluster[0])):
        #         if input("Is the device mobile or not.Give 1 for yes,else 0") ==1:
        #             specEachDevice.append(Mobile().setSpecification())
        #         else:
        #             specEachDevice.append(DeviceNode().setSpecification())
        #     #This is for the station(setting specfication)
        #     for i in range(int(cluster[1])):
        #         specEachDevice.append(DeviceNode().setSpecification())
        #     #
        #     deviceSpec_inCluster.append([specEachDevice,specEachStation])

        #Below when there can be only devices
        for  cluster,n_Devices in  enumerate(self.__devicePerCluster):
            #This variable is used to store the device specification per cluster
            specEachDevice_inCluster=[]
            print(f"\nGiving the device specfication for cluster {cluster}")
            for deviceno,n in enumerate(range(int(n_Devices))):
                print(f"For device {deviceno},Cluster {cluster}")
                if int(input("Is the device mobile or not.Give 1 for yes,else 0:")) ==1:
                    obj=Mobile()
                    obj.setSpecification(prompt=1)
                    specEachDevice_inCluster.append(obj)
                else:
                    obj=DeviceNode()
                    obj.setSpecification(prompt=1)
                    specEachDevice_inCluster.append(obj)
            #Appending of specEachDevice_inCluster forms the layer
            self.__deviceSpec_inLayer.append([specEachDevice_inCluster])



    #We will add standard specification for the devices and station
    #More info can be seen from eachDeviceSpecification()
    #All the devices here are assumed to be non-mobile
    def __standardSpecification(self):
        self.__deviceSpec_inLayer=[]
        for  n_Devices in  self.__devicePerCluster:
            #This variable is used to store the device specification per cluster
            specEachDevice_inCluster=[]
            for n in range(int(n_Devices)):
                obj=DeviceNode()
                obj.setSpecification()
                specEachDevice_inCluster.append(obj)
            #Appending of specEachDevice_inCluster forms the layer
            self.__deviceSpec_inLayer.append([specEachDevice_inCluster])

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
        print(f"Device Id".center(20," ")+"|"+f"ProcessingPower".center(20," ")+"|"+f"WattUsage".center(20," ")+"|"+f"Battery".center(20," ")+"|")
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
                    else:
                        battery="None".center(20," ")
                    print(f"{id}|{pp}|{watt}|{battery}|")
            




       

    
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
    
