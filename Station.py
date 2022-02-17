#This class is modelled to simply have a higher device specifications representing that of a high end commercial machine 
from DeviceNode import DeviceNode
class Station(DeviceNode):
    def __init__(self)->None:
        super().__init__(5000,32,1000,1000,1000,-1)
