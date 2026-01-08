from future_data import futureData
from get_data import getData
from prepare_data import prepareData
from study_data import studyData
import argparse


def getParams(symbol: str):
    return {
        "params": {
                "category": "spot",
                "symbol": symbol,
                "interval": "60",
                "limit": 1000,
                "start": "1293159702000"
            },
        "dirtFileData": f"data/dirt_data_{symbol}.json",
        "preparedFileData": f"data/prepared_data_{symbol}.json",
        "modelFile": f"data/model_{symbol}.keras",
        "scaledXFile": f"data/scaledX_{symbol}.save",
        "scaledYFile": f"data/scaledY_{symbol}.save"
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A script to process financial data for a given symbol.")
    parser.add_argument('-s', '--symbol', 
                        type=str, 
                        default="BTCUSDT",
                        help="The trading symbol to process (e.g., BTCUSDT)")
    
    args = parser.parse_args()
    symbol = args.symbol

    params = getParams(symbol)

    print("start: ", symbol)

    getData(params["params"], params["dirtFileData"])
    prepareData(params["dirtFileData"], params["preparedFileData"])
    studyData(params["preparedFileData"], params["modelFile"], params["scaledXFile"], params["scaledYFile"])
    futureData(params["params"], params["modelFile"], params["scaledXFile"], params["scaledYFile"])