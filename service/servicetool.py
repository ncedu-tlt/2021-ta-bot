import requests
import service.servicescfg as scfg
from service.servicepool import ServicePool
    
async def get(service_name: scfg.Service, params):

    url = await ServicePool.url(service_name)

    print(f"REQUEST STRING: {url}{service_name.value}/{params}")

    return requests.get(f"{url}{service_name.value}/{params}").json()
