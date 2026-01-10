from datetime import datetime
from enum import Enum
from consts import MACD_LONG
from dto import BuyType, Recomendation
from future_data import getFuture, loadModel, printRecommendation
from main_usdt import getParams
from prepare_data import getDirtData
import argparse

class StateType(Enum):
    FREE = 1
    SHORT = 2
    LONG =3

class HistoryState(Enum):
    PLUS = 1
    MINUS = 2
    FREE = 3

class History:
    plus: int
    minus: int

    maxPlus: int
    maxMinus: int

    def __init__(self):
        self.maxPlus = 0;
        self.maxMinus = 0
        self.plus = 0
        self.minus = 0



class State:
    stateType: StateType
    volume: float
    wallet: float
    sl: float
    tp: float
    ts: int
    currentPrice: float
    rec: Recomendation
    def __init__(self):
        self.stateType = StateType.FREE
        self.volume = 0
        self.wallet = 100
        self.sl = 0
        self.tp = 0
        self.currentPrice = 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A script to process financial data for a given symbol.")
    parser.add_argument('-s', '--symbol', 
                        type=str, 
                        default="BTCUSDT",
                        help="The trading symbol to process (e.g., BTCUSDT)")
    args = parser.parse_args()
    symbol = args.symbol

    params = getParams(symbol)

    dirtFile = params["dirtFileData"]
    scaledXFile = params["scaledXFile"]
    scaledYFile = params["scaledYFile"]
    modelFile = params["modelFile"]

    model, scaler_X, scaler_y = loadModel(modelFile, scaledXFile, scaledYFile)
    dirtData = getDirtData(dirtFile)

    print("start: ", symbol)

    state = State()


    history = History()
    historyState = HistoryState.FREE
    maxPlus = 0
    maxMinus = 0

    for index in range(MACD_LONG * 4, len(dirtData)-1):
        sliceDirt = dirtData[index - MACD_LONG * 3 : index]
        if state.stateType == StateType.FREE:
            results, lastCandle = getFuture(sliceDirt, model, scaler_X, scaler_y)
            avgMlPrice = lastCandle.closePrice
            if results.buyType == BuyType.Hold:
                continue
            if results.buyType == BuyType.Short or results.buyType == BuyType.Long:
                state.stateType = StateType.SHORT if results.buyType == BuyType.Short else StateType.LONG
                state.volume = state.wallet / avgMlPrice
                state.tp = results.tpMax
                state.sl = results.slMax
                state.ts = lastCandle.time
                state.currentPrice = avgMlPrice
                state.rec = results
                continue

        currentCandle = dirtData[index]

        if state.stateType == StateType.SHORT:
            if currentCandle.minPrice < state.tp or currentCandle.maxPrice > state.sl:
                state.stateType = StateType.FREE

                futurePrice = state.sl if currentCandle.maxPrice > state.sl else state.tp

                turnOverCurrent = state.volume * futurePrice
                turnOverPrev = state.volume * state.currentPrice

                nextWallet =  turnOverPrev + (turnOverPrev - turnOverCurrent)

                if nextWallet > state.wallet:
                    history.plus = history.plus + 1
                    if historyState == HistoryState.MINUS and maxMinus > history.maxMinus:
                        history.maxMinus = maxMinus
                    maxMinus = 0
                    if historyState == HistoryState.PLUS:
                        maxPlus = maxPlus +1
                    historyState = HistoryState.PLUS

                    print("++++++++++++++++++++++++++++++++++++++++")
                    printRecommendation(state.rec, symbol, sliceDirt[-1])

                else:
                    history.minus = history.minus + 1
                    if historyState == HistoryState.PLUS and maxPlus > history.maxPlus:
                        history.maxPlus = maxPlus
                    maxPlus = 0
                    if historyState == HistoryState.MINUS:
                        maxMinus = maxMinus +1
                    historyState = HistoryState.MINUS
                    print("-----------------------------------------")
                    printRecommendation(state.rec, symbol, sliceDirt[-1])



                state.wallet = nextWallet

                print("wallet: ", state.wallet)
                print(f"date: from {datetime.fromtimestamp(state.ts/1000)} to {datetime.fromtimestamp(currentCandle.time/1000)}")
                continue
        if state.stateType == StateType.LONG:
            if currentCandle.maxPrice > state.tp or currentCandle.minPrice < state.sl:
                state.stateType = StateType.FREE

                nextWallet = state.volume * (state.sl if currentCandle.minPrice < state.sl else state.tp)

                if nextWallet > state.wallet:
                    history.plus = history.plus + 1
                    if historyState == HistoryState.MINUS and maxMinus > history.maxMinus:
                        history.maxMinus = maxMinus
                    maxMinus = 0
                    if historyState == HistoryState.PLUS:
                        maxPlus = maxPlus +1
                    historyState = HistoryState.PLUS
                    print("++++++++++++++++++++++++++++++++++++++++")
                    printRecommendation(state.rec, symbol, sliceDirt[-1])
                else:
                    history.minus = history.minus + 1
                    if historyState == HistoryState.PLUS and maxPlus > history.maxPlus:
                        history.maxPlus = maxPlus
                    maxPlus = 0
                    if historyState == HistoryState.MINUS:
                        maxMinus = maxMinus +1
                    historyState = HistoryState.MINUS
                    print("-----------------------------------------")
                    printRecommendation(state.rec, symbol, sliceDirt[-1])

                state.wallet = nextWallet

                print("wallet: ", state.wallet)
                print(f"date: from {datetime.fromtimestamp(state.ts/1000)} to {datetime.fromtimestamp(currentCandle.time/1000)}")
                continue

    if state.stateType != StateType.FREE:
        currentCandle = dirtData[-1]
        currentAvg = currentCandle.getAvg()
        state.wallet = state.volume * currentAvg

    print("symbol: ", symbol)
    print("benefits: ", state.wallet)
    print("plus: ", history.plus, ", max plus: ", history.maxPlus)
    print("minus: ", history.minus, ", max minus: ", history.maxMinus)

