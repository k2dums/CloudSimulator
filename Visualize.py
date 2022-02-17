#This class is used for printing a particular Layer or the whole network
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from sympy import centroid
from Network import Network
from Layer import Layer
from NetworkConnection import NetworkConnection
import numpy as np
class Visualize:
    def __init__(self) -> None:
        style.use("fivethirtyeight")
        fig=plt.figure()
        ax1=fig.add_subplot(1,1,1)

    #Plots a particular layer with its clusterss
    #This shows the cluster connection within the layer if any
    def visualizeLayer(self,network,layerNo)->None:
        #First I need to get the layer
        assert isinstance(network,Network)
        layer=network.getNetworkLayers()
        layer=layer[layerNo]
        assert isinstance(layer,Layer)
        clusters=int(layer.getCluster())
        devicePerCluster=layer.getDevicePerCluster()
        connectionMatrix=layer.getConnectionMatrix()
        #xpos for created for offsetting between each cluster the offset value after each device cluster is later kept at 10
        #ylist for choosing a offset for the y position of the cluster 
        xpos=1
        ylist=[0,4]
        #These centroid x,centroid_y is for the storing the computed centroid value of the cluster
        centroid_x=0
        centroid_y=0
        #The centroid list is needed to keep a track of the centroid of each device cluster 
        centroid_xlist=np.array([])
        centroid_ylist=np.array([])
        #Plots the scatterd plot for the device,stations and the centroid of the cluster
        for  i  in range(clusters):
            ypos=ylist[np.random.randint(0,2)]
            cluster=devicePerCluster[i]
            devices=cluster[0]
            stations=cluster[1]
            x=(np.random.random_sample(size=devices)+xpos+0.6)
            y=(np.random.random_sample(size=devices)+ypos)
            centroid_x=sum(x)
            centroid_y=sum(y)
            c=np.random.rand(3)
            #Here the the clustered device is plotted as ^
            plt.scatter(x, y,color=c,marker='^',label=f"Devices in Cluster {i}")
            #Here plotting the stations as o
            x=(np.random.random_sample(size=stations)+xpos+0.6)
            y=(np.random.random_sample(size=stations)+ypos)
            plt.scatter(x, y,color=c,marker='o',label=f"Stations Cluster {i}")
            #Centroid Calculation
            centroid_x =(centroid_x+ sum(x))/(devices+stations)
            centroid_y =(centroid_y +sum(y))/(devices+stations)
            #Here the Centroid of the cluster is plotted as x
            plt.plot(centroid_x,centroid_y, marker= 'x',color="red")
            xpos+=10
            centroid_xlist=np.append(centroid_xlist,centroid_x)
            centroid_ylist=np.append(centroid_ylist,centroid_y)
        plt.legend(bbox_to_anchor=(-0.005,1.04), loc="upper right",fontsize=7)
        

        if not(hasattr(layer,"_Layer__connectionMatrix")):
            print("No connection within the cluster of the layer")
        #Else Plotting the connection(Lines plots) between clusters in a layer
        else:
            for clusterA in range(clusters):
                for clusterB in range (clusterA+1,clusters):
                    if connectionMatrix[clusterA][clusterB]==1:
                        plt.plot([centroid_xlist[clusterA],centroid_xlist[clusterB]],[centroid_ylist[clusterA],centroid_ylist[clusterB]],color='black', linewidth=1)
        plt.title(f"Layer {layerNo}")
        plt.show()


    #Plots the overall network with all the layer and its respective cluster
    #Omits the cluster connection within a layer
    def visualizeNetwork(self,network)->None:
        assert isinstance(network,Network)
        layers=network.getNetworkLayers()
        # no_ofLayers=network.getNumberofLayers()
        #x_refrence and y_refrence responsible for the offset of the scatter plot for its respective axis
        x_refrence=1
        y_refrence=0
        #This stores the list of centriod of a cluster in a layer
        centroidList_perLayer=[]
        #plotting all the layer and calulcating the centroid of each cluster in layer
        for layerno,layer in enumerate(layers):
            assert isinstance(layer,Layer)
            clusters=layer.getDevicePerCluster()
            cluster_centroid=[]
            x_refrence=1
            #Generating random colors based of rgb values
            c=np.random.rand(3)
            for cluster_no in range(layer.getCluster()):
                cluster=clusters[cluster_no]
                devices=cluster[0]
                stations=cluster[1]
                #Calcualating the x,y pos for the devices
                x=(np.random.random_sample(size=devices)+x_refrence+0.6)
                y=(np.random.random_sample(size=devices)+y_refrence) 
                #Calculting the centroid for the devices
                centroid_x=sum(x)
                centroid_y=sum(y)
                #Here the the clustered device is plotted as o
                plt.scatter(x, y,color=c,marker='o',label="")
                #Here plotting the stations as ^
                x=(np.random.random_sample(size=stations)+x_refrence+0.6)
                y=(np.random.random_sample(size=stations)+y_refrence)
                plt.scatter(x, y,color=c,marker='^',label=f"Layer {layerno}")
                #Centroid Calculation for a particular cluster
                centroid_x =(centroid_x+ sum(x))/(devices+stations)
                centroid_y =(centroid_y +sum(y))/(devices+stations)
                #In a layer list of clusters centroid (Seperating based on clusters)
                cluster_centroid.append([centroid_x,centroid_y])
                x_refrence+=10
            #List comprising of centriods of clusters within a layer(sepaerating based on layer)
            centroidList_perLayer.append(cluster_centroid)
            y_refrence+=4


 
        # Plotting the lines and making the connection between the various layers
        if not(hasattr(network,"_Network__connectionMatrix")):
            print("No connection between Layers formed")
        else:
            connectionMatrix_bwLayer=network.getConnectionMatrix()
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
        plt.title(f"Network {network.getNewtworkId()}")
        plt.show()
   



            

            
                
                





    