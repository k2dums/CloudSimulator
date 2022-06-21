from DeviceNode import DeviceNode
from Mobile import Mobile
from Station import Station
class Cluster:
    """
    Class is an abstraction of a cluster in a network\n
    A cluster serves as a container for the number of devices within in \n
    It has an attribute called weight , which is used in weighted Algorithms\n
    """
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
        """Adds device to the cluster\n
            it returns the added device instance\\n
        """
        obj=DeviceNode()
        self.devices.append(obj)
        return obj
    
    def addMobile(self):
        """Adds mobile instance to the cluster\n
           it returns the added mobile instance\\n        
        """
        obj=Mobile()
        self.devices.append(obj)
        return obj

    def addStation(self):
        """Adds station instance to the cluster\n
             it returns the added station instance\\n
        """
        obj=Station()
        self.devices.append(obj)
        return obj

    
    def makeDeviceConnections(self):
        """Makes the device connection within a cluster\n
            **Currently not functional just skeletion**\n
        """
        self.connectionMatrix=[]
        pass
    def getNoOfDevice(self):
        """Returns the number of devices in the cluster"""
        return len(self.devices)
    def getId(self):
        """Returns the cluster id"""
        return self.id
    def getDevices(self):
        """Returns the list device instances"""
        return self.devices
    def getWeight(self):
        """Gets the weight of the cluster"""
        return self.weight
    def setWeight(self,weight):
        """Sets the weight of the cluster"""
        self.weight=weight
        return self.weight


    def getUtilization(self):
        """Returns the utilizaiotn of the cluster \n
           Based on wether the device is occupied or not\n
        """
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
        """Returns True if a device in the cluster 
        has a task else False\n
        """
        for device in self.devices:
            assert isinstance(device,DeviceNode)
            if device.getResourceList():
                return True
        return False

    def getActiveDeviceNo(self):
        """Returns the number of active devices in the cluster"""
        activeNo=0
        for device in self.getDevices():
            assert isinstance(device,DeviceNode)
            if device.getStatus()==DeviceNode.READY or device.getStatus()==DeviceNode.PROCESSING or device.getStatus()==DeviceNode.SUCCESS:
                activeNo+=1
        return activeNo
    def getNonActiveDevices(self):
        """Returns teh number of non active devices in the cluster"""
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
        



