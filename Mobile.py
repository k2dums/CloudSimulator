from typing import Final
from DeviceNode import DeviceNode

class Mobile(DeviceNode):
    #Here we are assuming the nominal voltage of the mobile device to be around 3.7
    __NOM_VOLTAGE:Final=3.7
    __deviceId=1
    def __init__(self) -> None:
        #the battery capacity eg 4000mAh
        self.__batteryCapacity=-1
        #the eneergy of the battery stored
        self.__batteryEnergy=-1
        
    
    def getBatteryEnergy(self):
        return self.__batteryEnergy
    
    #Function that drain the batery energy based on time
    def drainBattery(self,time:float=1) ->None:
        self.__batteryEnergy-= self.__wattDuringLoad()*time/60
        #Here we assume the Depth of Discharge for the battery is 100%

    #Function computes the present load of the device and the power usage of the device in Watt
    def __wattDuringLoad(self):
        return (self.__batteryCapacity/100)* Mobile.__NOM_VOLTAGE
    
    def getConfig(self)->None:
        super().getConfig()
        print("Battery Capacity:",self.__batteryCapacity)
        print("Nominal Voltage:",Mobile.__NOM_VOLTAGE)
        print("Battery Energy:",self.__batteryEnergy)
        print("\n\n")
    
    def setSpecification(self,processingPower=2000,ram=4,memory=500,downloadRate=100,uploadRate=100,batteryCapacity=4000)->None:
        self.__batteryCapacity=batteryCapacity
        self.__batteryEnergy=self.__batteryCapacity
        powerWatt=self.__wattDuringLoad()
        super().__init__(Mobile.__deviceId,processingPower,ram,memory,downloadRate,uploadRate,powerWatt)
        Mobile.__deviceId+=1
        
        
mobile1=Mobile()
mobile1.setSpecification()
mobile2=Mobile()
mobile2.setSpecification()
mobile1.drainBattery(100)


mobile1.getConfig()
mobile2.getConfig()





        