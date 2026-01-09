from datetime import datetime
from enum import Enum
from consts import MACD_LONG
from dto import BuyType
from future_data import getFuture, loadModel
from main_usdt import getParams
from prepare_data import getDirtData
import argparse

class StateType(Enum):
    FREE = 1
    SHORT = 2
    LONG =3

class State:
    stateType: StateType
    volume: float
    wallet: float
    sl: float
    tp: float
    ts: int
    currentPrice: float
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

    plus = 0
    minus = 0

    for index in range(MACD_LONG * 4, len(dirtData)-1):
        sliceDirt = dirtData[index - MACD_LONG * 3 : index]
        if state.stateType == StateType.FREE:
            results, lastCandle = getFuture(sliceDirt, model, scaler_X, scaler_y)
            avgMlPrice = lastCandle.getAvg()
            if results.buyType == BuyType.Hold:
                continue
            if results.buyType == BuyType.Short or results.buyType == BuyType.Long:
                state.stateType = StateType.SHORT if results.buyType == BuyType.Short else StateType.LONG
                state.volume = state.wallet / avgMlPrice
                state.tp = results.tpMax
                state.sl = results.slMax
                state.ts = lastCandle.time
                state.currentPrice = avgMlPrice
                continue

        currentCandle = dirtData[index]
        currentAvg = currentCandle.getAvg()

        if state.stateType == StateType.SHORT:
            if currentAvg < state.tp or currentAvg > state.sl:
                state.stateType = StateType.FREE

                futurePrice = state.tp if currentAvg < state.tp else state.sl

                turnOverCurrent = state.volume * futurePrice
                turnOverPrev = state.volume * state.currentPrice

                nextWallet =  turnOverPrev + (turnOverPrev - turnOverCurrent)

                if nextWallet > state.wallet:
                    plus = plus + 1
                else:
                    minus = minus + 1

                state.wallet = nextWallet

                print("wallet: ", state.wallet)
                print(f"date: from {datetime.fromtimestamp(state.ts/1000)} to {datetime.fromtimestamp(currentCandle.time/1000)}")
                continue
        if state.stateType == StateType.LONG:
            if currentAvg > state.tp or currentAvg < state.sl:
                state.stateType = StateType.FREE

                nextWallet = state.volume * (state.tp if currentAvg > state.tp else state.sl)

                if nextWallet > state.wallet:
                    plus = plus + 1
                else:
                    minus = minus + 1

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
    print("plus: ", plus)
    print("minus: ", minus)

