

from NetworkConnection import NetworkConnection
from Layer import Layer,Cluster,DeviceNode,Mobile,Station,np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
class Network:
    """
    This class keeps a track of all the layer created \n
    The layer object manipulated here\n
    This class also makes the connection between the the cluster of the a layer and cluster of different layer\n
    """
    #Statiac variable to track the network id
    __NETWORK_ID=0
    #The layerid needs to be passed during the creation of a layaer and updated likewise
    def __init__(self) -> None:
        #This sets the network id of the network data structure=[Layer object,Layer object ]
        self.__networkId=Network.__NETWORK_ID
        #This keeps a track of the layers in the network
        self.__networkLayers=np.array([])
        #this keeps a track of the layerid , here it is important to pass it to the Layer object and value is incremented in the Network Class
        self.__layerId=0
        Network.__NETWORK_ID+=1
    
    
    def createAndLayerSpecs(self):
        """Creates the layer and asks for the specification of the layer"""
        n_layers=int(input("Give the number of Network Layers : "))
        for i in range (n_layers):
            self.createLayer()
        self.layerSpecs()
  
    def createLayer(self):
        """
          This creates a network object put inside  list to keep a track of the layers in a network\n
        """
        layer=Layer(self.__getLayerId())
        self.__updateLayerId()
        self.__networkLayers=np.append(self.__networkLayers,layer)
        return layer

    def layerSpecs(self):
        """Asks the specification for the layer"""
        for layer in self.__networkLayers:
            assert isinstance(layer,Layer)
            layer.inputData()
            return
    
    def printAllLayerSummary(self):
        """
        This prints the all layer in a network and its  summary including the clusters and its devices\n
        """
        if len(self.__networkLayers)==0:
            print("Error:Printing Layer Summary {Zero Layers Present}")
            return 
        print('\n\n')
        print(f"All Layer Summary-Network {self.__networkId}".center(100," "))
        for layer in self.__networkLayers:
            assert isinstance(layer,Layer)
            layer.printLayerSummary()

  
    def printLayerSummary(self,layerNo=0):
        """  This prints the layer summary of a particular network """
        if len(self.__networkLayers)==0:
            print("Error:Printing Layer Summary {Zero Layers Present}")
            return 
        if layerNo > len(self.__networkLayers):
            print("Error:Unable to print LayerSummary { Layer "+str(layerNo)+" OutOfBounds}")
            return
        for layer in self.__networkLayers:
            assert isinstance(layer,Layer)
            if layer.getId()==layerNo:
                layer.printLayerSummary()
    
   
    def makeLayerConnections(self):
        """
         Sets the connection between layers in a network\n
         Connection are allowed only between adjacent layer\n
        """
        if len(self.__networkLayers)==1:
            print("There is only one layer,no network connection created")
            return
        print(f"\nConnection Specification for the Network {self.__networkId}")
        #This is for the connection between the cluster layer of a layer to the cluster layer of another layer
        self.__connectionMatrix=[]
        for layerA in range(len(self.__networkLayers)):
            layerconnection=[]
            for layerB in range(layerA+1):
                if layerA==layerB:
                    layerconnection.append(0)
                else:
                    layerconnection.append(-1)

            for layerB in range(layerA+1,len(self.__networkLayers)):
                if layerA==layerB-1:#This only allows a layer connection with the very  next layer
                    connection=NetworkConnection(layerA,layerB,self.__networkLayers[layerA],self.__networkLayers[layerB])
                else :
                    connection=0
                layerconnection.append(connection)
            self.__connectionMatrix.append(layerconnection)
        
    def getUtilization(self):
        """Returns  the  overall utiilization for the network """
        utilization=0
        layers=self.getNetworkLayers()
        n_layers=len(layers)
        for layer in layers:
            assert isinstance(layer,Layer)
            utilization+=layer.getUtilzation()
        utilization/=n_layers
        return utilization

    def getUtilzationPerLayer(self):
        """Returns the utilization of each layer in the network"""
        utilizationPerLayer=[]
        layers=self.getNetworkLayers()
        for layer in layers:
            assert isinstance(layer,Layer)
            utilizationPerLayer.append(layer.getUtilzation())
        return utilizationPerLayer
    
    def getUtilizationPerLayerPerCluster(self):
        """Returns the utilization of each cluster of each layer in a"""
        layers=self.getNetworkLayers()
        networkUtilization=[]
        for layer in layers:
            assert isinstance(layer,Layer)
            networkUtilization.append(layer.getUtilizationPerCluster())
        return networkUtilization
          

    

    # #Creates cluster connection between a particular layer
    # def makeClusterConnectioninLayer(self):
    #     layers=network.getNetworkLayers()
    #     userInput=input("Give the layers which you like to make cluster connection within its layer (seperate with ,) ")
    #     userInput=userInput.split(",")
    #     for layerno in userInput:
    #         layer=layers[layerno]
    #         assert isinstance(layer,Layer)
    #         layer.makeClusterConnection()
    
   
    def visualizeNetwork(self)->None:
        """
         Plots the overall network with all the layer and its respective cluster\n
         Omits the cluster connection within a layer\n
        """
        style.use("fivethirtyeight")
        layers=self.getNetworkLayers()
        # no_ofLayers=network.getNumberofLayers()
        #x_refrence and y_refrence responsible for the offset of the scatter plot for its respective axis
        x_refrence=1
        y_refrence=0
        #This stores the list of centriod of a cluster in a layer
        centroidList_perLayer=[]
        #plotting all the layer and calulcating the centroid of each cluster in layer
        for layerno,layer in enumerate(layers):
            assert isinstance(layer,Layer)
            clusters=layer.getClusters()
            cluster_centroid=[]
            x_refrence=1
            #Generating random colors based of rgb values
            c=np.random.rand(3)
            for cluster in layer.getClusters():
                assert isinstance(cluster,Cluster)
                n_devices=len(cluster.getDevices())
                #Calcualating the x,y pos for the devices
                x=(np.random.random_sample(size=n_devices)+x_refrence+0.6)
                y=(np.random.random_sample(size=n_devices)+y_refrence) 
                #Calculting the centroid for the devices
                centroid_x=sum(x)
                centroid_y=sum(y)
                #Here the the clustered device is plotted as o
                plt.scatter(x, y,color=c,marker='o',label=f"cluster {cluster.getId()}")
                # #Here plotting the stations as ^
                # x=(np.random.random_sample(size=stations)+x_refrence+0.6)
                # y=(np.random.random_sample(size=stations)+y_refrence)
                # plt.scatter(x, y,color=c,marker='^',label=f"Layer {layerno}")
                #Centroid Calculation for a particular cluster
                centroid_x =centroid_x /n_devices
                centroid_y =centroid_y /n_devices
                #In a layer list of clusters centroid (Seperating based on clusters)
                cluster_centroid.append([centroid_x,centroid_y])
                x_refrence+=10
            #List comprising of centriods of clusters within a layer(sepaerating based on layer)
            centroidList_perLayer.append(cluster_centroid)
            y_refrence+=4
            
        # Plotting the lines and making the connection between the various layers
        if not(hasattr(self,"_Network__connectionMatrix")):
            print("No connection between Layers formed")
        else:
            connectionMatrix_bwLayer=self.getConnectionMatrix()
            #Now to get the connection status(if value =1 for clusters in different layer) and based on it plotting lines
            for layerA_no in range(len(connectionMatrix_bwLayer)-1):#If there is 4 layers it can make 3 connection between layers
                layerNext=layerA_no+1
                layerA=connectionMatrix_bwLayer[layerA_no]#We get the connectin status  for the particular layer(connection status is given by Network Connection object )
                NC_obj=layerA[layerNext]#We get the network connection for a layer and the next layer (this tells us which clusters are to be connected)
                assert isinstance(NC_obj,NetworkConnection)
                NC_connection=NC_obj.getNetworkConnection()#This returns a  conncetion matrix of the layer clusters and the layerNext clusters
                # print(f"Setting up connection between Layer{NC_obj.getFrom()}  and Layer {NC_obj.getTo()}")
                for clusterA_no,clusterA in enumerate(NC_connection):
                    for clusterB_no,clusterB in enumerate(clusterA):
                        if NC_connection[clusterA_no][clusterB_no]==1:#if connection status between clusters of differnt layers =1 plot line
                            #We plot lines based on the centroid of the clusters of the layers
                            layerA_ref=centroidList_perLayer[layerA_no]
                            layerB_ref=centroidList_perLayer[layerNext]
                            x=0
                            y=1
                            x1=layerA_ref[clusterA_no][x]
                            y1=layerA_ref[clusterA_no][y]
                            x2=layerB_ref[clusterB_no][x]
                            y2=layerB_ref[clusterB_no][y]
                            plt.plot([x1,x2],[y1,y2],color='black',linewidth=1)

        plt.legend(bbox_to_anchor=(-0.005,1.04), loc="upper right",fontsize=7)
        plt.title(f"Network {self.getNewtworkId()}")
        plt.show()
   
    
    def dummyNetwork(self):
        """
        Function creates a layer (one layer)\n
        Adds 3 cluster each having 3 devices\n
        Since the device is created in Standard the ProcessingPower=4000\n
        """
        self.createLayer()
        layer0=self.getNetworkLayers()[0]
        assert isinstance(layer0,Layer)
        layer0.dummyCluster()
    
    def copyNetwork(self,network):
        """Copies the network configuraition of the network passed as parameter"""
        for layer in network.getNetworkLayers():
            assert isinstance(layer,Layer)
            _layer=self.createLayer()
            for cluster in layer.getClusters():
                _cluster=_layer.addCluster()
                for device in cluster.getDevices():
                    assert isinstance(device,DeviceNode)
                    device_copy=None
                    if isinstance(device,Mobile):
                        device_copy=_cluster.addMobile()
                    elif isinstance(device,Station):
                        device_copy=_cluster.addStation()
                    elif isinstance(device,DeviceNode):
                        device_copy=_cluster.addDevice()
                    if not(layer.getisStandard()):
                        _layer.setisStandard(False)
                        assert isinstance(device_copy,DeviceNode)
                        device_copy._DeviceNode__setProcessingPower(device.getProcessingPower())
                        device_copy._DeviceNode__setDeviceId(device.getDeviceId())
                        device_copy._DeviceNode__setRam(device.getRam())
                        device_copy._DeviceNode__setMemory(device.getMemory())
                        device_copy._DeviceNode__setDownloadRate(device.getDownloadRate())
                        device_copy._DeviceNode__setUploadRate(device.getUploadRate())
                        device_copy._DeviceNode__setPowerWatt(device.getPowerWatt())
                        device_copy._DeviceNode__setInstructionLength(device.getInstructionLength())

                        if isinstance(device_copy,Mobile):
                            device_copy._Mobile__setBatteryCapacity(device.getBatteryCapcity())



              







      



    
    def __getLayerId(self)->int:
        """Returns the layer id of the network"""
        return self.__layerId
    def __updateLayerId(self)->None:
        """Updates the layer id, this is passed during layer initiatlization"""
        self.__layerId+=1
    def getNetworkLayers(self)->list[Layer]:
        """Returns the list of network layers instances"""
        return self.__networkLayers
    def getConnectionMatrix(self):
        """Returns the connection Matrix """
        return self.__connectionMatrix
    def getNumberofLayers(self)->int:
        """Returns the number of layers in network"""
        return len(self.__networkLayers)
    def getNewtworkId(self)->int:
        """Returns the network id """
        return self.__networkId
    def resetTaskAllocated(self):
        """Resets the task allocated the devices in the network"""
        if not(self.getNetworkLayers()):
            return
        if self.getNumberofLayers()<=0:
            return
        layer0=self.getNetworkLayers()[0]
        assert isinstance(layer0,Layer)
        for cluster in layer0.getClusters():
            assert isinstance(cluster,Cluster)
            for device in cluster.getDevices():
                assert isinstance(device,DeviceNode)
                device.resetTask()
    def debugPrint(self):
        print("I am Network")

# if __name__=="__main__":
#       network=Network()
#       network.createLayer()
#       network.makeLayerConnections()

        


    

