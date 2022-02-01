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
-	[ ] Testing the addition of multiple layer and their connection
-	[ ] Plotting the Whole Network
-	[ ] Shutting down of device when battery down
-	[ ] Allocation of a resource to a  device in a cluster or the whole cluster
-	[ ] Calculating the time taken for the processing by the cluster
-	[ ] Probability of device shutting down  
-	[ ] Reallocation of the resources to another device in cluster or to a next cluster
-	[ ] Calculating the latency(Bandwidth between the layers, clusters, devices)
## Datastructures used in various classes
##### Layer class in Layer.py
self.__deviceSpec_inLayer is a list in function __eachDeviceSpecfication()
Overall DataStructure  for an cluster entity in self.__deviceSpec_inLayer:
[   [ [devices,stations]  ]        ]
For two cluster in the self.__deviceSpec_inLayer:
[  [devices,stations ]  ,   [devices,stations ]   ]
[   ____cluster1______  ,   ____cluster2_______   ]

##### Network class in Network.py
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
