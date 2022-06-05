from DeviceNode import DeviceNode
from Mobile import Mobile
from Station import Station
class Cluster:
    def __init__(self,id) -> None:
        self.id=id
        self.devices=[]
        self.weight=-1
        # self.connectionMatrix=[]
    def __str__(self) -> str:
        return f'Cluster {self.id}'
    
    def __repr__(self) -> str:
        return f'Cluster {self.id}'
        
        

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
    
    def isThereTask(self):
        for device in self.devices:
            assert isinstance(device,DeviceNode)
            if device.getResourceList():
                return True
        return False

    def getActiveDeviceNo(self):
        activeNo=0
        for device in self.getDevices():
            assert isinstance(device,DeviceNode)
            if device.getStatus()==DeviceNode.READY:
                activeNo+=1
        return activeNo
    def getNonActiveDevices(self):
        nonActive=[]
        for device in self.getDevices():
            assert isinstance(device,DeviceNode)
            if (device.getStatus()==DeviceNode.CREATED) or (device.getStatus()==DeviceNode.IDLE) or (device.getStatus()==DeviceNode.SUCCESS):
                nonActive.append(device)
        return nonActive
        

if __name__=='__main__':
    cluster=Cluster(1)
    for i in range(10):
        cluster.addDevice()
    print("Device",cluster.getNoOfDevice())
    devices=cluster.getDevices()
    for i in range(5):
        device=devices[i]
        assert isinstance(device,DeviceNode)
        device.setStatus(DeviceNode.READY)
    print(cluster.getActiveDeviceNo())
        



