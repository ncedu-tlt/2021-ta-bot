from fsm.statebroker import StateBroker

class FSMCustom:

    def __init__(self):
        self.__state = None        
        self.__cluster_name = "Default"
        self.__cluster = None
        self.__start_container_index = 0
        self.__container_index = self.__start_container_index

    def setup(self, cluster: str = "Default"):
        self.__cluster = StateBroker.pick_out_cluster(cluster)
    
    def get_data(self, state: str):
        state_data = StateBroker.containerOf(state, self.__cluster_name).dataOf()
        return state_data
    
    def update_data(self, state: str, new_data):
        state_data = StateBroker.containerOf(state, self.__cluster_name).set_data(new_data)
        return state_data 

    def enter(self, state):
        container_index = StateBroker.container_index(state)
        self.__container_index = container_index
        container = StateBroker.find_container_by_index(container_index)
        self.__state = container.stateInfo()


    def name(self, state):
        container_index = StateBroker.container_index(state)
        self.__container_index = container_index
        container = StateBroker.find_container_by_index(container_index)
        return container.state_nameInfo()

    def next(self):

        if StateBroker.find_container_by_index(self.__container_index  + 1) != None:           
            container = StateBroker.find_container_by_index(self.__container_index + 1)
            self.__state = container.stateInfo()  
            self.__container_index += 1
           
        else:                       
            container = StateBroker.find_container_by_index(self.__start_container_index)            
            self.__state = container.stateInfo()       
            self.__container_index = self.__start_container_index
            

    def back(self):
        if StateBroker.find_container_by_index(self.__container_index  - 1) != None:           
            container = StateBroker.find_container_by_index(self.__container_index - 1)  
            self.__state = container.stateInfo()             
            self.__container_index -= 1   
            
           
        else:   
            last_index = len(StateBroker.container_all()) - 1
            container = StateBroker.find_container_by_index(last_index)            
            self.__state = container.stateInfo()      
            self.__container_index = last_index


    def current(self):
        return self.__state