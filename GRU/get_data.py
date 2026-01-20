import json
import requests
from consts import BI_BIT_API
from dto import DirtData
from datetime import datetime

from utils import convertFromStockToData, getArrayFromResponse

def getData(params, dirtFileData):
    print("start", datetime.fromtimestamp(int(params["start"])/1000))
    response = getArrayFromResponse(requests.get(BI_BIT_API, params=params).json())
    array: list[DirtData] = []

    while len(response) > 1:
        print("len:", len(response))
        response.reverse()
        for item in response:
            nextData = convertFromStockToData(item)
            array.append(nextData)
        newParams = params.copy()
        newTime = array[len(array)-1].time + 1;
        newParams["start"]=newTime
        response = getArrayFromResponse(requests.get(BI_BIT_API, params=newParams).json())
        dt_utc = datetime.fromtimestamp(newTime/1000)
        print(dt_utc)
    jsonStr = jsonStr = json.dumps([item.to_dict() for item in array])
    with open(dirtFileData, "w", encoding="utf-8") as file_data:
        file_data.write(jsonStr)




    
