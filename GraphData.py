
import numpy as np
class GraphData:
    def __init__(self) -> None:
        # self.__clusters=5
        # self.__station=5
        # self.__devicePerCluster=[10,5,10,20,7]
        # self.__connectionMatrix=[]
        self.inputData()
    
    def inputData(self):
        self.__clusters=int(input("Give the number of Clusters:"))
        self.__station=int(input("Give the number of stations:"))
        self.__devicePerCluster=np.array([])
        print(type(self.__devicePerCluster))
        #Here we are allocating devices per cluster
        for i in range(self.__clusters):
            devices=int(input(f"For Cluster {i} give the number of devices:"))
            self.__devicePerCluster=np.append(self.__devicePerCluster,devices)
        #Now we need connection ,see if they are connected
        #By default a cluster cannot connect directly to another cluster
        #Here the connection_matrix is simply to find to connection of station to cluster
        self.__connectionMatrix=np.zeros((self.__station,self.__clusters))
        print("If Connection exist give 1 else 0 \n")
        for i in range(self.__station):
            for j in range(self.__clusters):
                print(f'Connection between station {i} and cluster {j}:')
                value=-1
                while value!=0 and value!=1 :
                    value=int(input("Connection value=:"))
                    if value!=0 and value!=1:
                        print("Error with the connection value try again:")
                print("\n")
                self.__connectionMatrix[i][j]=value
            
                
    

    def printData(self):
        print("Station:",self.__station)
        print("Clusters",self.__clusters)
        print("Device Per Cluster",self.__devicePerCluster)
        print("Connection Matrix:\n",self.__connectionMatrix)
    
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
    
