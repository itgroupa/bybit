import requests
from consts import BI_BIT_API, INPUT, MACD_LONG, MACD_SHORT, WINDOW
from dto import DirtData, MiddleData
from datetime import datetime, timedelta
import tensorflow as tf
import joblib
import numpy as np

from utils import convertFromStockToData, getArrayFromResponse, getXMiddle

def futureData(params, modelFile, scaledXFile, scaledYFile):
    newParams = params.copy()
    prevTs = (datetime.now() - timedelta(days=4)).timestamp() * 1000
    newParams["start"] = int(prevTs)

    print("start", datetime.fromtimestamp(int(newParams["start"])/1000))

    response = getArrayFromResponse(requests.get(BI_BIT_API, params=newParams).json())
    dirtData: list[DirtData] = []
    response.reverse()

    for item in response:
        nextData = convertFromStockToData(item)
        dirtData.append(nextData)
    print("data len: ", len(dirtData))

    model = tf.keras.models.load_model(modelFile)

    model.summary()

    scaler_X = joblib.load(scaledXFile)
    scaler_y = joblib.load(scaledYFile)

    array: list[MiddleData] = []
    for index in range(MACD_LONG, len(dirtData) -  1):
        current = dirtData[index]
        prev = dirtData[index - 1]
        longMacd = dirtData[index - MACD_LONG: index]
        shortMacd = dirtData[index - MACD_SHORT: index]
        newVal = MiddleData(current, prev, shortMacd, longMacd)
        array.append(newVal)

    transformedData = getXMiddle(array);
    raw_X = np.array(transformedData)  # (N, 11)

    print("raw_X: ", len(raw_X))

    X_last = raw_X[-WINDOW:]
    X_last_scaled = scaler_X.transform(X_last)
    X_last_scaled = X_last_scaled.reshape(1, WINDOW, INPUT)

    
    y_pred_scaled = model.predict(X_last_scaled)
    y_pred = scaler_y.inverse_transform(y_pred_scaled)

    lastCandle = dirtData[-1]
    future = y_pred[0]
    print("coin: ", params["symbol"])
    print("current date: ", datetime.fromtimestamp(lastCandle.time/1000))

    print("")

    print("current open: ", lastCandle.openPrice)
    print("current close: ", lastCandle.closePrice)
    print("current max: ", lastCandle.maxPrice)
    print("current min: ", lastCandle.minPrice)
    print("current price: ", lastCandle.getAvg())

    print("")

    print("next open: ", lastCandle.openPrice - future[0])
    print("next close: ", lastCandle.closePrice - future[1])
    print("next max: ", lastCandle.maxPrice - future[2])
    print("next min: ", lastCandle.minPrice - future[3])
    print("next price: ", lastCandle.getAvg() - future[4])

    print("")


    print("good luck")




    
