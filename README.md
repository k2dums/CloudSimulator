
# Cloud Simulator
## CheckList
-	[x] Cluster and no of cluster in devices
-   [x] Stations and their connection to the cluster
-   [x] Visualization of the connection of the cluster devices and stations
-	[x] Configuring  the processing power of each device in a cluster
-	[x] Creating a Battery parameter to the mobile 
-	[x] Printing Summary of a Layer
-	[x] Adding Layers to the network
-	[x] Each Layer has number of clusters
-   [x] Layers can have station and devices
-	[x] Testing the addition of multiple layer and their connection
-	[x] Plotting the Whole Network
-	[ ] Shutting down of device when battery down
-	[x] Allocation of a resource to a  device in a cluster or the whole cluster
-	[x] Calculating the time taken for the processing by the cluster
-	[ ] Probability of device shutting down  
-	[ ] Reallocation of the resources to another device in cluster or to a next cluster
-	[ ] Calculating the latency(Bandwidth between the layers, clusters, devices)
-   [ ] Using latency and memory characteristics of a device
-   [ ] Objective function using energy consumption 

## Datastructures used in various Classes


##### Network class in Network.py
<pre>
self.__connectionMatrix in makeLayerConnections()
Overall DataStructure for self.__connectionMatrix
[ [layer0],[layer1]...[layern] ]
for layer 0
[ [NC_Layer0 NC_layer1 NC_Layer2  ]]  NC is NetworkConnection Obj
Therefore a layer entity in self.__connectionMatrix
[ [NC_Layeri  NC_Layer(i+1) NC_Layer(i+2] ]
Therefore two layer in self.__connectionMatrix
[ [NC_layer NC_Layer NC_Layer]  , [NC_layer NC_Layer NC_layer] ]
[ ________Layer1_____________   , _________Layer2_____________ ]    
</pre>


##### NetworkConnection class in NetworkConnection.py
<pre>
self.__conenction in makeConnection()
This is a matrix created by taking the clusters number in two layers
say Layer1=3 cluster, Layer2=2cluster therefore 3x2 matrix is created
the rows correspond the number of cluster in layerA (the lower layer)
the cols correspond the cluster number in layerB(the upper layer)
</pre>
