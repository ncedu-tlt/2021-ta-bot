
class StateContainer:

    def __init__(self, state, name, data = None, cluster: str = "Default"):       
        self.__name = name
        self.__data = data
        self.__cluster = cluster
        self.__index = 0
        self.__state = state
        StateBrokerContainer(self)

    def nameOf(self):
        return self.__name
    
    def dataOf(self):
        return self.__data

    def clusterOf(self):
        return self.__cluster
   
    def indexOf(self):
        return self.__index

    def set_data(self, new_data):
        self.__data = new_data
    
    def set_index(self, index):
        self.__index = index
    
    def stateOf(self):       
        return self.__state

class StateBrokerContainer():
    def __init__(self, container: StateContainer):
        self.__container = container
        StateBroker.pack_cluster(self, self.__container.clusterOf())
        
    def containerOf(self):
        return self.__container
    
    def containerInfo(self):
        string = f"\nCONTAINER INFO:\nCONTAINER INDEX: {self.__container.indexOf()}\nSTATE: {self.__container.nameOf()}\nDATA: {self.__container.dataOf()}\nCluster: {self.__container.clusterOf()}\n"
        return string
    
    def state_nameInfo(self):
        return self.__container.nameOf()

    def stateInfo(self):
        return self.__container.stateOf()        

    def indexing(self, index):
        self.__container.set_index(index)

    def indexOf(self):
        return self.__container.indexOf()


class StateBroker:
    
    __clusters = dict()
        
    @staticmethod
    def pack_cluster(container: StateBrokerContainer, cluster = "Default"):
        
        proxy_list = list()  

        try:     

            if StateBroker.__clusters[cluster] != None:
                proxy_list = StateBroker.__clusters[cluster]
                proxy_list.append(container)                
                StateBroker.__clusters[cluster] = proxy_list
                StateBroker.indexing_container()

        except: 
            StateBroker.__clusters[cluster] = list()
            StateBroker.__clusters[cluster].append(container)   
            StateBroker.indexing_container()


    @staticmethod
    def cluster_info(cluster = "Default"):
        cluster = StateBroker.__clusters[cluster]
        
        
    @staticmethod
    def clusters_info():
        return StateBroker.__clusters

    @staticmethod
    def pick_out_cluster(cluster = "Default"):
        print(f"Picking out from '{cluster}' cluster")
        return StateBroker.__clusters[cluster]
    
    @staticmethod
    def state_nameOf(state: str, cluster: str = "Default"):        
        for container in StateBroker.__clusters[cluster]:                       
            if container.state_nameInfo() == state:                
                return container.state_nameInfo()

    @staticmethod
    def stateOf(state, cluster: str = "Default"):
        for container in StateBroker.__clusters[cluster]:            
            if container.stateInfo() == state:
                return container.stateInfo()


    @staticmethod
    def containerOf(state: str, cluster: str = "Default"):
        for container in StateBroker.__clusters[cluster]:
            if container.stateInfo() == state:
                return container.containerOf()
    
    @staticmethod
    def container_all(cluster: str = "Default"):
        return StateBroker.__clusters[cluster]
    

    @staticmethod
    def indexing_container(cluster: str = "Default"):       
        for x in range(len(StateBroker.__clusters[cluster])):
            StateBroker.__clusters[cluster][x].indexing(x)
    
    @staticmethod
    def container_index(state, cluster: str = "Default"):
        for container in StateBroker.__clusters[cluster]:
            if container.stateInfo() == state:
                return container.indexOf()
    
    @staticmethod
    def find_container_by_index(index, cluster: str = "Default"):        
        
        if index < len(StateBroker.__clusters[cluster]):
            
            for container in StateBroker.__clusters[cluster]:
                if container.indexOf() == index:
                    return container
        else:
            return None
    