import dicttool
from config import MARKS
import requests


async def comments(response, count, output_str):

    for each in response:
        mark = await dicttool.find_similarities(MARKS, each['mark'])
        output_str += f"{count}.\t\tОценка:\t\t{mark}/5\n{each['review']}\n\n"
        count += 1
    
    return output_str

async def user_comments(responce, count, output_str):
    for each in responce:
        output_str += f"{count}.\t\t{each['namePlace']}\t\tОценка:\t\t{each['mark']}/5\t\tНомер: {each['id']}\n{each['review']}\n\n"
        count += 1
    
    return output_str