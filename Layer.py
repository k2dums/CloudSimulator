

import numpy as np
from Cluster import Cluster,DeviceNode,Mobile,Station



class Layer:
    """
    Layer Connection matrix  is used for the connection between clusters \n
    The LayerId static variable needs to be part of the Network class\n
    """
    def __init__(self,layerId) -> None:
        self.__layerId=layerId
        self.__clusters=[]
        self.__clusterId=0
        self.__weight=-1
        self.__isStandard=True
    
    def __repr__(self) -> str:
        return f'Layer {self.__layerId}'
    def __str__(self) -> str:
        return f'Layer {self.__layerId}'
        
    

    def inputData(self):
        """
            This is  for  getting  inital input for the number of cluster,devices and stations
        """
        print("\n")
        print(f"Layer-{self.__layerId} Config")
        self.askCluster()
        self.deviceSpecInLayer()
   
    def askCluster(self):
        """Asks the number of cluster in that layer to be added """
        noOfClusters=int(input(f"Give the number of Clusters in Layer-{self.__layerId} : "))
        for i in range(noOfClusters):
            self.addCluster()
           

        
    
    def addCluster(self):
            """Creating of n number of  Cluster in a Layer"""
            cluster=Cluster(self.setClusterId())
            self.__clusters.append(cluster)
            return cluster
            

    def deviceSpecInLayer(self):
        """Specification for the device such as standard or manual\n
           for standard all the default arguments will be given\n
           while manual , needs to set the device characterstics\n
        """
        standard_spec=input(f"'y' for Standard Specification for the device,else 'n' for manual specification : ").lower()
        while standard_spec!='y' and standard_spec !='n':
            print("Error:Invalid User Input")
            standard_spec=input(f" 'y' for Standard Specification for the device,else manual specification,else 'n' : ").lower()

        #For standard specification for the device
        if standard_spec == 'y':
            for cluster in self.__clusters:
                assert isinstance(cluster,Cluster)
                n_devices=int(input(f"Give the number of Devices in Cluster-{cluster.getId()}-Layer {self.__layerId} : "))
                for i in range(n_devices):
                    cluster.addDevice()

        #For manual specification for the device
        elif standard_spec == 'n':
            self.setisStandard(False)
            detailed_spec=input("'y' for a  detailed specification, else 'n' : ").lower()
            while detailed_spec !='y' and detailed_spec!='n':
                print("Error:Invalid User Input")
                detailed_spec=input("'y' for a detailed specification, else 'n' : ").lower()

            for cluster in self.__clusters:
                assert isinstance(cluster,Cluster)
                n_devices=int(input(f"Give the number of Devices in Cluster-{cluster.getId()}-Layer {self.__layerId} : "))

                for i in range(n_devices):
                    print(f"Specs for Device {i} in Cluster {cluster.getId()}-Layer {self.getId()}")
                    device_type=input(f"if device Mobile give 'm', Device give 'd', Station give 's' : ").lower()
                    while  device_type!='s' and  device_type!='d' and  device_type!='m':
                        print("Error:Invalid Input from User")
                        print(f"if device Mobile give 'm', Device give 'd', Station give 's' : ")
                        device_type=input().lower()
                  
                    if device_type == 'd':
                        device=cluster.addDevice()
                        assert isinstance(device,DeviceNode)
                        if detailed_spec=='y':
                            device.setSpecification()
                            
                    elif device_type == 's':
                        station=cluster.addStation()
                        assert isinstance (station,Station)
                        if detailed_spec=='y':
                            station.setSpecification()
                    elif device_type == 'm':
                        mobile=cluster.addMobile()
                        assert isinstance(mobile,Mobile)
                        if detailed_spec=='y':
                            mobile.setSpecification()


    #This is sets the connection for the __clusters within a particular layer
    # def makeConnection(self):
    #     #Now we need connection ,see if they are connected
    #     #Here the connection_matrix is simply to find to connection of clsuter to cluster
    #     self.__connectionMatrix=np.zeros((self.__clusters,self.__clusters))
    #     print("If Connection exist give 1 else 0")
    #     for i in range(self.__clusters):
    #         for j in range(i+1):
    #             if i==j:
    #                 continue
    #             else:
    #                 self.__connectionMatrix[i][j]=-1
    #         for j in range(i+1,self.__clusters):
    #             print(f'Connection between cluster {i} and cluster {j}:')
    #             value=-1
    #             while value!=0 and value!=1 :
    #                 value=int(input("Connection value=:"))
    #                 if value!=0 and value!=1:
    #                     print("Error with the connection value try again:")
    #         self.__connectionMatrix[i][j]=value
 





 
    def printAbstractData(self):
        """
        Was used for debugging to print the layer charactersitics
        """
        print('layer id',self.__layerId)
        print("No of Clusters",len(self.__clusters))
        print('utilzation',self.__utilzation)
        print("Utilization per cluster ",self.__utilzationPerCluster)

    
  
    def printLayerSummary(self):
        """
        Prints the summary details of all the device in a particular layer
        """
        print("\n")
        print(f"Layer-{self.__layerId} Summary".center(100," "))
        print(f"Device Id".center(20," ")+"|"+f"Processing Power".center(20," ")+"|"+f"WattUsage".center(20," ")+"|"+f"Battery".center(20," ")+"|"+f"Type".center(20," "))
        for cluster in self.__clusters:
            assert isinstance(cluster,Cluster)
            print(f"Cluster-{cluster.getId()}".center(75," "))
            for device in cluster.getDevices():
                assert isinstance(device,DeviceNode)
                id:str=f'{device.getDeviceId()}'.center(20," ")
                pp:str=f'{device.getProcessingPower()}'.center(20," ")
                watt:str=f'{device.getPowerWatt()}'.center(20," ")
                if isinstance(device,Mobile):
                    battery=f'{device.getBatteryCapcity()}'.center(20," ")
                    type="Mobile"
                else:
                    battery="None".center(20," ")
                    if isinstance(device,Station):
                        type="Station"
                    elif isinstance(device,DeviceNode):
                        type="Non Mobile"
                type=type.center(20," ")
                print(f"{id}|{pp}|{watt}|{battery}|{type}")
            




    #The setter and getter for the attributes of the Layer class
    def getId(self):
        """Returns the layer id"""
        return self.__layerId
    def setClusterId(self):
        """Sets the cluster id , this id is passed during cluster initialzation"""
        self.updateClusterId()
        return self.__clusterId-1
    def getClusters(self)->list[Cluster]:
        """Returns the list of cluster instances"""
        return self.__clusters
    def getNoClusters(self):
        """Returns the number of cluster in the layer"""
        return len(self.__clusters)
    def getUtilzation(self):
        """Returns the utiliatioln of the cluster"""
        temp=0
        n=len(self.__clusters)
        for cluster in self.__clusters:
            assert isinstance(cluster,Cluster)
            temp+=cluster.getUtilization()
        utilzation=temp/n
        return utilzation
    def getUtilizationPerCluster(self):
        """Returns the utilizaiton per cluster in a layer """
        utilizationPerCluster=[]
        for cluster in self.__clusters:
            assert isinstance(cluster,Cluster)
            utilizationPerCluster.append(cluster.getUtilization())
        return utilizationPerCluster
    def setWeight(self,weight):
        """Sets the weight of the layer"""
        self.__weight=weight
        return self.__weight
    def getWeight(self):
        """Gets the weight of the layer"""
        return self.__weight
    def updateClusterId(self):
        """Updates the cluster id, by incrementing by 1"""
        self.__clusterId+=1
    def getisStandard(self):
        """Returns true, if the specification was set in standard else False"""
        return self.__isStandard
    def setisStandard(self,flag:bool):
        """Sets the varaible isStandard to the flag"""
        self.__isStandard=flag
        
        
#     def getConnectionMatrix(self):
#         return self.__connectionMatrix

   
    def dummyCluster(self):
        """Creates teh dummy cluster for testing purpose\n
           Creates 3 cluster and adds 3 devices to each cluster\n
        """
        cluster1=Cluster(0)
        cluster2=Cluster(1)
        cluster3=Cluster(2)
        self.__clusters.append(cluster1)
        self.__clusters.append(cluster2)
        self.__clusters.append(cluster3)
        for cluster in self.__clusters:
            for i in range(3):
                assert isinstance(cluster,Cluster)
                cluster.addDevice()
        

if __name__=='__main__':
    print(dir())