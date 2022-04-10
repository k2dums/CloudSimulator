from DeviceNode import DeviceNode
from Mobile import Mobile
from Station import Station
class Cluster:
    def __init__(self,id) -> None:
        self.id=id
        self.devices=[]
        self.weight=-1
        # self.connectionMatrix=[]
        

    def addDevice(self):
        obj=DeviceNode()
        self.devices.append(obj)
        return obj
    
    def addMobile(self):
        obj=Mobile()
        self.devices.append(obj)
        return obj

    def addStation(self):
        obj=Station()
        self.devices.append(obj)
        return obj

    
    def makeDeviceConnections(self):
        self.connectionMatrix=[]
        pass
    def getNoOfDevice(self):
        return len(self.devices)
    def getId(self):
        return self.id
    def getDevices(self):
        return self.devices
    def getWeight(self):
        return self.weight
    def setWeight(self,weight):
        self.weight=weight
        return self.weight


    def getUtilization(self):
        n=len(self.devices)
        if n==0:
            return -1
        occupied=0
        for device in self.devices:
            assert isinstance(device,DeviceNode)
            status=device.getStatus()
            if status!=DeviceNode.CREATED and status!=DeviceNode.FAILED and status!=DeviceNode.FAILED_RESOURCE_UNAVAILABLE:
                occupied+=1
        utilization=occupied/n
        return utilization

    def getActiveDeviceNo(self):
        activeNo=0
        for device in self.devices():
            assert isinstance(device,DeviceNode)
            if device.getStatus==DeviceNode.READY:
                activeNo+=1
        return activeNo
        




