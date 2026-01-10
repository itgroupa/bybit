from datetime import datetime
import json

from consts import MACD_DAYS, MACD_HOURS, MACD_LONG, MACD_MIDDLE, NEXT_PERIOD
from dto import DirtData, PreparedData

def getDirtData(dirtFileData):
    dirtData: list[DirtData]
    with open(dirtFileData, 'r', encoding='utf-8') as f:
        dirtData = [DirtData(**item) for item in json.load(f)]
    return dirtData;

def prepareData(dirtFileData, preparedFileData):

    dirtData = getDirtData(dirtFileData)

    print("prepared data len: ", len(dirtData))
    print("start time: ", datetime.fromtimestamp(dirtData[0].time/1000))
    array: list[PreparedData] = []
    for index in range(MACD_LONG, len(dirtData) - NEXT_PERIOD -  1):
        current = dirtData[index]
        prev = dirtData[index - 1]
        longMacd = dirtData[index - MACD_LONG: index]
        middleMacd = dirtData[index - MACD_MIDDLE: index]
        daysMacd = dirtData[index - MACD_DAYS: index]
        hoursMACD = dirtData[index - MACD_HOURS: index]
        nextData = dirtData[index : index + NEXT_PERIOD]
        newVal = PreparedData.create(current, prev, hoursMACD, daysMacd, middleMacd, longMacd, nextData)
        array.append(newVal)
    jsonStr = jsonStr = json.dumps([item.to_dict() for item in array])
    with open(preparedFileData, "w", encoding="utf-8") as file_data:
        file_data.write(jsonStr)