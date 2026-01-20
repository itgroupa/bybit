import requests
from consts import BI_BIT_API, INPUT, MACD_LONG, MACD_HOURS, MACD_DAYS, MACD_MIDDLE, WINDOW
from dto import DirtData, MiddleData, Recomendation, TargetType
from datetime import datetime, timedelta
import tensorflow as tf
import joblib
import numpy as np

from utils import convertFromStockToData, getArrayFromResponse, getXMiddle

def printRecommendation(results: Recomendation, symbol: str, lastCandle: DirtData, targetType: TargetType):
    print("coin: ", symbol)
    print("current date: ", datetime.fromtimestamp(lastCandle.time/1000))

    print("")

    print("current open: ", lastCandle.openPrice)
    print("current close: ", lastCandle.closePrice)
    print("current max: ", lastCandle.maxPrice)
    print("current min: ", lastCandle.minPrice)
    print("current price: ", lastCandle.getAvg())

    print("")

    print(f"recomendation type {results.buyType}")
    print("next price: ", f"{results.avgPrice}, procents: {results.diffProcent:.4f}%")
    print("tp price: ", f"{results.tp}, procents: {results.diffBenefit:.4f}%")
    print("tp price max: ", f"{results.tpMax}, procents: {results.diffTpMax:.4f}%")
    print("sl price: ", f"{results.sl}, procents: {results.diffLose:.4f}%")
    print("sl price max: ", f"{results.slMax}, procents: {results.diffSlMax:.4f}%")
    print(f"dirrection: {results.direction}, strategy type: {targetType}")

def loadModel(modelFile, scaledXFile, scaledYFile):
    model = tf.keras.models.load_model(modelFile)

    model.summary()

    scaler_X = joblib.load(scaledXFile)
    scaler_y = joblib.load(scaledYFile)

    return model, scaler_X, scaler_y

def getFuture(dirtData: list[DirtData], model, scaler_X, scaler_y, targetType: TargetType):

    array: list[MiddleData] = []
    for index in range(MACD_LONG, len(dirtData) - 1):
        current = dirtData[index]
        prev = dirtData[index - 1]
        longMacd = dirtData[index - MACD_LONG: index]
        hoursMacd = dirtData[index - MACD_HOURS: index]
        daysMacd = dirtData[index - MACD_DAYS: index]
        middleMacd = dirtData[index - MACD_MIDDLE: index]
        newVal = MiddleData(current, prev, hoursMacd, daysMacd, middleMacd, longMacd)
        array.append(newVal)

    transformedData = getXMiddle(array)
    raw_X = np.array(transformedData)

    X_last = raw_X[-WINDOW:]

    X_last_reshaped = X_last.reshape(-1, INPUT)
    X_last_scaled = scaler_X.transform(X_last_reshaped)
    X_last_scaled = X_last_scaled.reshape(1, WINDOW, INPUT)

    y_pred_scaled = model.predict(X_last_scaled, verbose=0)
    y_pred = scaler_y.inverse_transform(y_pred_scaled)

    lastCandle = dirtData[-1]
    future = y_pred[0]

    results = Recomendation(lastCandle, future, targetType)
    return results, lastCandle



def futureData(params, modelFile, scaledXFile, scaledYFile, targetType: TargetType):
    newParams = params.copy()
    prevTs = (datetime.now() - timedelta(days=3)).timestamp() * 1000
    newParams["start"] = int(prevTs)

    print("start", datetime.fromtimestamp(int(newParams["start"])/1000))

    response = getArrayFromResponse(requests.get(BI_BIT_API, params=newParams).json())
    dirtData: list[DirtData] = []
    response.reverse()

    for item in response:
        nextData = convertFromStockToData(item)
        dirtData.append(nextData)
    print("data len: ", len(dirtData))

    model, scaler_X, scaler_y = loadModel(modelFile, scaledXFile, scaledYFile)
    results, lastCandle = getFuture(dirtData, model, scaler_X, scaler_y, targetType)

    printRecommendation(results, params["symbol"], lastCandle, targetType)

    print("")


    print("good luck")




    
