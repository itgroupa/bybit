from datetime import datetime
import json

from consts import MACD_LONG, MACD_SHORT, NEXT_PERIOD
from dto import DirtData, PreparedData

def getDirtData(dirtFileData):
    dirtData: list[DirtData]
    with open(dirtFileData, 'r', encoding='utf-8') as f:
        dirtData = [DirtData(**item) for item in json.load(f)]
    return dirtData;

def prepareData(dirtFileData, preparedFileData):

    dirtData = getDirtData(dirtFileData)

    print("prepared data len: ", len(dirtData))
    print("open price [0]: ", dirtData[0].openPrice)
    print("start time: ", datetime.fromtimestamp(dirtData[0].time/1000))
    array: list[PreparedData] = []
    for index in range(MACD_LONG, len(dirtData) - NEXT_PERIOD -  1):
        current = dirtData[index]
        prev = dirtData[index - 1]
        longMacd = dirtData[index - MACD_LONG: index]
        shortMacd = dirtData[index - MACD_SHORT: index]
        nextData = dirtData[index : index + NEXT_PERIOD]
        newVal = PreparedData.create(current, prev, shortMacd, longMacd, nextData)
        array.append(newVal)
    jsonStr = jsonStr = json.dumps([item.to_dict() for item in array])
    with open(preparedFileData, "w", encoding="utf-8") as file_data:
        file_data.write(jsonStr)