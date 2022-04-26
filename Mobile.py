#This class is modelled to have a battery within the device and its needed behaviours
from typing import Final
from DeviceNode import DeviceNode

class Mobile(DeviceNode):
    #Here we are assuming the nominal voltage of the mobile device to be around 3.7
    __NOM_VOLTAGE:Final=3.7
    def __init__(self) -> None:
        #the battery capacity eg 4000mAh
        self.__batteryCapacity=4000
        #the eneergy of the battery stored
        self.__batteryEnergy=self.__batteryCapacity
        super().__init__(900)
    
 
        
    
    
    
    #Function that drain the batery energy based on time
    def drainBattery(self,time:float=1) ->None:
        self.__batteryEnergy-= self.__wattDuringLoad()*time/60
        #Here we assume the Depth of Discharge for the battery is 100%

    #Function computes the present load of the device and the power usage of the device in Watt
    def __wattDuringLoad(self)->float:
        return (self.__batteryCapacity/100)* Mobile.__NOM_VOLTAGE
    
   
   #This sets the specification for the instnace of the mobile object (has extra battery parameter) 
    def setSpecification(self,processingPower=2000,ram=4,memory=500,downloadRate=100,uploadRate=100,batteryCapacity=4000)->None:
        powerWatt=self.__wattDuringLoad
        processingPower=int(input("Give the processing power in MIPs:"))
        user=input("Would you like to give more details for the device ,'y' for yes else 'n': ").lower()
        while user !='y' and user !='n':
            print("Error:Invalid User Input")
            user=input("Would you like to give more details for the device ,'y' for yes else 'n': ").lower()
        if(user=='y'):
            ram=int(input("Give the RAM size in GB:"))
            memory=int(input("Give the Memory space in GB:"))
            downloadRate=int(input("Give the download Rate in Mbps:"))
            uploadRate=int(input("Give the Upload Rate in Mbps:"))
            batteryCapacity=int(input("Give the battery capacity in MAh:"))
        powerWatt=self.__wattDuringLoad()
        self._DeviceNode__setProcessingPower(processingPower)
        self._DeviceNode__setRam(ram)
        self._DeviceNode__setMemory(memory)
        self._DeviceNode__setDownloadRate(downloadRate)
        self._DeviceNode__setUploadRate(uploadRate)
        self._DeviceNode__setPowerWatt(powerWatt)
        self.__setBatteryCapacity(batteryCapacity)



    #Setter and getters for the Mobile class attributes
    def getBatteryCapcity(self):
        return self.__batteryCapacity
    def getBatteryEnergy(self):
        return self.__batteryEnergy 
    def __setBatteryCapacity(self,bc:int):
        self.__batteryCapacity=bc
        self.__batteryEnergy=bc
    def getConfig(self)->None:
        super().getConfig()
        print("Battery Capacity:",self.__batteryCapacity)
        print("Nominal Voltage:",Mobile.__NOM_VOLTAGE)
        print("Battery Energy:",self.__batteryEnergy)
        print("\n\n")

if __name__ == "__main__":
    obj=Mobile()
    print(dir(obj))

        