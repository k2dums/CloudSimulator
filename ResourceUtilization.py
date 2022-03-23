from http.client import FAILED_DEPENDENCY
from DeviceNode import DeviceNode
from Layer import Layer
from DeviceNode import DeviceNode
class ResourceUtilization():

    def utilzationReport(layer):
        assert isinstance(layer,Layer)
        utilzationPerCluster=[]
        avg_utilization=0
        layers=layer.getdeviceSpec_inLayer()
        no_cluster=len(layers)
        for cluster in layers:
            no_devices=0
            occupied=0
            for devices in cluster:
                no_devices=len(devices)
                for obj in devices:
                    assert isinstance(obj,DeviceNode)
                    status=obj.getStatus()
                    if status!=DeviceNode.CREATED or status!=DeviceNode.FAILED or status !=FAILED_DEPENDENCY:
                        occupied+=1
            utilzationPerCluster.append(occupied/no_devices)
            avg_utilization+=occupied/no_devices
        avg_utilization/=no_cluster
        return avg_utilization,utilzationPerCluster

        
        
                    



        
        