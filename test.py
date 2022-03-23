
from sympy import centroid
from Network import Network
from Layer import Layer

cenntroid_list=[    [    [2.1114357389424865, 0.5216633364888509]  ,    [12.05889442877167, 0.48298240240806567]     ], [   [2.148202169217106, 4.045971677483179]  ]  ]
# cenntroid_list=[   [ ['C1x','C1y'],['C2x,C2y'] ] ,[   ['C1x','C1y']    ]      ]
#                                       -----------CLUSTER 1--------------------- , --------------CLUSTER 2-------------------                    ---------------CLUSTER 1------------------
#                                 ----------------------------LAYER 1---------------------------------------------------------------        -----------------LAYER 2------------------------------
print(cenntroid_list)
#My connection give the layer Refrencenntroid_list
layernoA=0
layernext=layernoA+1

firstConnection=cenntroid_list[layernoA]
print("First Connection",firstConnection)
secondConnection=cenntroid_list[layernext]
print("Second Connection",secondConnection)
print(len(firstConnection))
print(len(secondConnection))

clusterno=1
print(firstConnection[clusterno])
print(firstConnection[clusterno][0])
print(firstConnection[clusterno][1])