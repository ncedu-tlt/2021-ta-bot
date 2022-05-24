from fsm.statebroker import StateContainer

class State:
    
    def __init__(self, name, data = None, cluster: str = "Default"):
        self.__name = name
        StateContainer(self, self.__name, data, cluster)
        
