from dto import TargetType
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
                "interval": "15",
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
    parser.add_argument('-tt', '--targetType', 
                        type=lambda x: TargetType[x],
                        choices=list(TargetType),
                        default=TargetType.Common,
                        help="Target Type (Common, Hard, Soft)")
    parser.add_argument('-w', '--work', 
                        action='store_true',
                        help="with study")
    
    args = parser.parse_args()
    symbol = args.symbol
    study = args.work
    targetType = args.targetType

    print("with study: ", study)
    print("target type: ", targetType)
    params = getParams(symbol)

    print("start: ", symbol)

    if study:
        getData(params["params"], params["dirtFileData"])
        prepareData(params["dirtFileData"], params["preparedFileData"])
        studyData(params["preparedFileData"], params["modelFile"], params["scaledXFile"], params["scaledYFile"])
    futureData(params["params"], params["modelFile"], params["scaledXFile"], params["scaledYFile"], targetType)