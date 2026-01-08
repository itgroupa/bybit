from dto import DirtData, MiddleData, PreparedData

def getArrayFromResponse(data):
    return data.get("result", {}).get("list", [[]])

def convertFromStockToData(val):
    return DirtData(int(val[0]), 
                    float(val[1]), 
                    float(val[4]), 
                    float(val[2]), 
                    float(val[3]), 
                    float(val[5]), 
                    float(val[6])) #'1767578880000', '3188.21', '3188.75', '3185.3', '3187.94', '122.88134', '391643.474781'
                                   #"timestamp", "open", "high", "low", "close", "volume", "turnover"
def getXPrepared(val: list[PreparedData]):
    result = []
    for item in val:
        result.append([item.price,
            item.macdCurrent,
            item.volume])
    return result;

def getYPrepared(val: list[PreparedData]):
    result = []
    for item in val:
        result.append([item.avgOpenNext,
            item.avgCloseNext,
            item.avgMaxNext,
            item.avgMinNext,
            item.avgPriceNext])
    return result;

def getXMiddle(val: list[MiddleData]):
    result = []
    for item in val:
        result.append([item.price,
            item.macdCurrent,
            item.volume])
    return result