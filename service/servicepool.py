from service.servicescfg import SERVICE_URL

class ServicePool:

    pool = dict()

    @staticmethod    
    def create():
        ServicePool.pool = SERVICE_URL
    
    @staticmethod
    async def printpool():
        print(ServicePool.pool)
    
    @staticmethod
    async def url(name):       
        return ServicePool.pool[name]
