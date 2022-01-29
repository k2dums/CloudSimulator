from DeviceNode import DeviceNode
class Station(DeviceNode):
    def __init__(self)->None:
        super().__init__(5000,32,1000,1000,1000,-1)
