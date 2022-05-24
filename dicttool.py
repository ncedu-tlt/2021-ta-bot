
async def list_keys(data: dict):       
    keys = [key for key in data.keys()]    
    return keys


async def list_values(data: dict):
    values = [value for value in data.values()]
    return values


async def has_key(data: dict, key):
    for x in data.keys():
        if x == key:
            return True
        
    return False


async def find_in(data: list, key):
    for x in data:
        if await has_key(x, key) == True:
            return True
    
    return False


async def get_value_by_key(data: dict, key):
    return data[key]


async def find_similarities(src_data: dict, data: dict):
    for x in src_data.keys():
        for y in data.values():
            if x == y:
                return src_data[y]