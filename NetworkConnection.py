from Layer import Layer,Cluster
class NetworkConnection:
    """
    This class is reponsible to keep a track of the cluster\n
    which is connected to another cluster in another layer\n
    Since a layer can have mulitple clusters ,therefore need to track\n
    which cluster is connecting to which cluster between two layers\n
    from Layer import Layer,Cluster,np\n
    """
    def __init__(self,start,end,layerA,layerB) -> None:
        assert isinstance(layerA,Layer) and isinstance(layerB,Layer)
        self.__layerA=layerA
        self.__layerB=layerB
        self.__connection=np.zeros( ( layerA.getNoClusters(), layerB.getNoClusters() ) )
        self.makeConnection()
   
    
    def makeConnection(self):
        """
        this function makes the connection between clusters of two layers(adjacent)
        """
        print(f"\nSetting up connection betweene Layer {self.__layerA.getId()} and Layer {self.__layerB.getId()}")
        print("[y] for Connection else [n]")                  
        layerA=self.__layerA
        layerB=self.__layerB
        assert isinstance(layerA,Layer)
        assert isinstance(layerB,Layer)
        for clusterA in layerA.getClusters():
            for clusterB in layerB.getClusters():
                assert isinstance(clusterA,Cluster) and isinstance(clusterB,Cluster)
                print( f"Connection between Layer-{layerA.getId()}-Cluster{clusterA.getId()} and Layer{layerB.getId()}-Cluster {clusterB.getId()}" )
                userInput="None"
                while not(userInput == "y") and not(userInput == "n"):
                    userInput=input()
                    if not(userInput=='y') and not(userInput=='n'):
                        print("Input Error: give a valid input")
                if userInput=='y':
                    self.__connection[clusterA.getId()][clusterB.getId()]=1
                elif userInput=='n':
                    self.__connection[clusterA.getId()][clusterB.getId()]=0
                    

                
                
                
        
    
    #Setters and getters for the NetworkConnection Class
    def getFrom(self)->None:
        """
        Gets the id  of starting  layer
        """
        return self.__layerA.getId()

    def getTo(self)->None:
        """
        Gets the id of  next layer
        """
        return self.__layerB.getId()
    def getNetworkConnection(self):
        """
        Returns the connection matrix between two layers 
        """
        return self.__connection