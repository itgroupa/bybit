from dataclasses import dataclass

@dataclass
class DirtData:
    time: int
    openPrice: float
    closePrice: float
    maxPrice: float
    minPrice: float
    volume: float
    turnOver: float
    def __init__(self, time: int, openPrice: float, closePrice: float, maxPrice: float, minPrice: float, volume: float, turnOver: float):
        self.time = time
        self.openPrice = openPrice
        self.closePrice = closePrice
        self.maxPrice = maxPrice
        self.minPrice = minPrice
        self.volume = volume
        self.turnOver = turnOver
    def to_dict(self):
        return {
            "time": self.time,
            "openPrice": self.openPrice,
            "closePrice": self.closePrice,
            "maxPrice": self.maxPrice,
            "minPrice": self.minPrice,
            "volume": self.volume,
            "turnOver": self.turnOver
        }
    def getAvg(self):
        return (self.openPrice + self.closePrice) / 2
    def getAvgOpen(self):
        return self.getAvg() - self.openPrice
    def getAvgClose(self):
        return self.getAvg() - self.closePrice
    def getAvgMax(self):
        return self.getAvg() - self.maxPrice
    def getAvgMin(self):
        return self.getAvg() - self.minPrice

class MiddleData:
    time: int
    price: float
    macdCurrent: float
    volume: float
    
    def __init__(self, current: DirtData, 
                 prev: DirtData, 
                 macdCurrentShort: list[DirtData], 
                 macdCurrentLong: list[DirtData]):
        self.time = current.time
        self.volume = current.volume
        self.price = current.getAvg() / prev.getAvg()
        macdCurrentTemp = sum(item.getAvg() for item in macdCurrentShort) / len(macdCurrentShort) -  sum(item.getAvg() for item in macdCurrentLong) / len(macdCurrentLong)
        self.macdCurrent = macdCurrentTemp

@dataclass
class PreparedData:
    time: int
    price: float
    macdCurrent: float
    volume: float
    avgOpenNext: float
    avgCloseNext: float
    avgMaxNext: float
    avgMinNext: float
    avgPriceNext: float

    def __init__(self, time: int,
        price: float,
        macdCurrent: float,
        volume: float,
        avgOpenNext: float,
        avgCloseNext: float,
        avgMaxNext: float,
        avgMinNext: float,
        avgPriceNext: float):
            self.time = time
            self.price = price
            self.macdCurrent = macdCurrent
            self.volume = volume
            self.avgOpenNext = avgOpenNext
            self.avgCloseNext = avgCloseNext
            self.avgMaxNext = avgMaxNext
            self.avgMinNext = avgMinNext
            self.avgPriceNext = avgPriceNext

    def create(current: DirtData, 
                 prev: DirtData, 
                 macdCurrentShort: list[DirtData], 
                 macdCurrentLong: list[DirtData],
                 nextData: list[DirtData]):
        temNewVal = MiddleData(current, prev, macdCurrentShort, macdCurrentLong)
        
        time = temNewVal.time
        volume = temNewVal.volume
        price = temNewVal.price
        macdCurrent = temNewVal.macdCurrent
        avgOpenNext = current.openPrice - sum(item.openPrice for item in nextData) / len(nextData)  
        avgCloseNext = current.closePrice - sum(item.closePrice for item in nextData) / len(nextData)
        avgMaxNext = current.maxPrice - max(item.maxPrice for item in nextData)
        avgMinNext = current.minPrice - min(item.minPrice for item in nextData)
        avgPriceNext = current.getAvg() - sum(item.getAvg() for item in nextData) / len(nextData)
        

        return PreparedData(time,
            price,
            macdCurrent,
            volume,
            avgOpenNext,
            avgCloseNext,
            avgMaxNext,
            avgMinNext,
            avgPriceNext)


    def to_dict(self):
        return {
            "time": self.time,
            "price": self.price,
            "macdCurrent": self.macdCurrent,
            "volume": self.volume,
            "avgOpenNext": self.avgOpenNext,
            "avgCloseNext": self.avgCloseNext,
            "avgMaxNext": self.avgMaxNext,
            "avgMinNext": self.avgMinNext,
            "avgPriceNext": self.avgPriceNext
        }
