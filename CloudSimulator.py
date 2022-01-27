
from DeviceNode import DeviceNode
from Layer import Layer
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np



style.use("fivethirtyeight")
fig=plt.figure()
ax1=fig.add_subplot(1,1,1)


def animate(data):
    clusters=int(data.getCluster())
    devicePerCluster=data.getDevicePerCluster()
    connectionMatrix=data.getConnectionMatrix()
    stations=int(data.getStation())
    #xpos for created for offsetting between each cluster the offset value after each device cluster is later kept at 10
    #ylist for choosing a offset for the y position of the cluster 
    xpos=1
    ylist=[0,4]
    #These centroid x,centroid_y is for the storing the computed centroid value of the clustr
    centroid_x=0
    centroid_y=0
    #The centroid list is needed to keep a track of the centroid of each device cluster 
    centroid_xlist=np.array([])
    centroid_ylist=np.array([])
    #Plots the scatterd plot for the device cluster
    for  i  in range(clusters):
        ypos=ylist[np.random.randint(0,2)]
        devices=int(devicePerCluster[i])
        x=(np.random.random_sample(size=devices)+xpos+0.6)
        y=(np.random.random_sample(size=devices)+ypos)
        centroid_x=sum(x)/devices
        centroid_y=sum(y)/devices
        c=np.random.rand(3)
        #Here the the clusterd device is plotted as ^
        plt.scatter(x, y,color=c,marker='^',label=f"Cluster {i}")
        #Here the Centroid of the device is plotted as x
        plt.plot(centroid_x,centroid_y, marker= 'x',color="red")
        xpos+=10
        centroid_xlist=np.append(centroid_xlist,centroid_x)
        centroid_ylist=np.append(centroid_ylist,centroid_y)
    plt.legend(bbox_to_anchor=(-0.005,1.04), loc="upper right",fontsize=7)
    
    
    #Offsets are needed to place them right or left to the refrence centriod(values from staionx,staiony)
    offsetleft=20
    offsetright=20
    stationx=sum(centroid_xlist)/clusters
    stationy=sum(centroid_ylist)/clusters+5

    #Plotting the Stations as Dot with the text of the Station no
    for i in range(stations):
        if i ==0:
            plt.plot(stationx,stationy,marker="o")
            plt.text(stationx,stationy,f"Station {i}",horizontalalignment='center',verticalalignment='center',fontsize=7)
        elif i%2==0:
            plt.plot(stationx +offsetright,stationy,marker="o")
            plt.text(stationx +offsetright,stationy,f"Station {i}",horizontalalignment='center',verticalalignment='center',fontsize=7)
            offsetright+=20
        else:
            plt.plot(stationx -offsetleft,stationy,marker="o")
            plt.text(stationx -offsetleft,stationy,f"Station {i}",horizontalalignment='center',verticalalignment='center',fontsize=7)
            offsetleft+=20
  
    #The offset values are reset to 20 since these values are again needed to plot the line connection
    offsetleft=20
    offsetright=20
    stationYpos=stationy
    stationXpos=-1
    #Now we making the connection (Line plots) between the clusters and the station
    for stationNo in range(len(connectionMatrix)):
        if stationNo==0:
            stationXpos=stationx
        elif  stationNo%2==0:
            stationXpos=stationx+offsetright
            offsetright+=20
        else:
            stationXpos=stationx-offsetleft
            offsetleft+=20
        for clusterNo in range(len(connectionMatrix[stationNo])):
            if connectionMatrix[stationNo][clusterNo]==1:
               
                plt.plot([centroid_xlist[clusterNo],stationXpos],[centroid_ylist[clusterNo],stationYpos-0.2],color='black',linewidth=1)

    plt.show()
            
        
if __name__ == "__main__":
   layer=Layer()
   animate(layer)
   layer.specificationRequest()
   layer.printLayerData()
