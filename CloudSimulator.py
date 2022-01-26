
from DeviceNode import DeviceNode
from GraphData import GraphData
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np



style.use("fivethirtyeight")
fig=plt.figure()
ax1=fig.add_subplot(1,1,1)


def animate(graphData):
    clusters=int(graphData.getCluster())
    devicePerCluster=graphData.getDevicePerCluster()
    connectionMatrix=graphData.getConnectionMatrix()
    stations=int(graphData.getStation())
    xpos=1
    ylist=[0,4]
    centroid_x=0
    centroid_y=0
    centroid_xlist=np.array([])
    centroid_ylist=np.array([])
    for  i  in range(clusters):
        ypos=ylist[np.random.randint(0,2)]
        devices=int(devicePerCluster[i])
        x=(np.random.random_sample(size=devices)+xpos)
        y=(np.random.random_sample(size=devices)+ypos)
        centroid_x=sum(x)/devices
        centroid_y=sum(y)/devices
        c=np.random.rand(3)
        plt.scatter(x, y,color=c,marker="x",label=f"Cluster {i}")
        plt.plot(centroid_x,centroid_y, marker= '^',color="red")
        xpos+=10
        centroid_xlist=np.append(centroid_xlist,centroid_x)
        centroid_ylist=np.append(centroid_ylist,centroid_y)
    plt.legend(bbox_to_anchor=(-0.005,1.04), loc="upper right",fontsize=7)
    
    
    #Now plotting the Station
    offsetleft=20
    offsetright=20
    stationx=sum(centroid_xlist)/clusters
    stationy=sum(centroid_ylist)/clusters+5

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
  
    
    offsetleft=20
    offsetright=20
    stationYpos=stationy
    stationXpos=-1
    #Now we making the connection between the clusters and the station
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
    
            
    print("Connection Matrix:\n",connectionMatrix)
    plt.show()
            
        
        
    



if __name__ == "__main__":
   graphData=GraphData()
   animate(graphData)
