from dataclasses import dataclass
from enum import Enum

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
        return (self.closePrice + self.openPrice) / 2
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
    macdCurrentHours: float
    macdCurrentDays: float
    macdCurrentMiddle: float
    macdCurrentLong: float
    volume: float
    
    def __init__(self, current: DirtData, 
                 prev: DirtData, 
                 macdCurrentHours: list[DirtData],
                 macdCurrentDays: list[DirtData], 
                 macdCurrentMiddle: list[DirtData], 
                 macdCurrentLong: list[DirtData]):
        self.time = current.time
        self.volume = current.volume
        self.price = current.getAvg() - prev.getAvg()
        self.macdCurrentHours = current.getAvg() - sum(item.getAvg() for item in macdCurrentHours) / len(macdCurrentHours)
        self.macdCurrentDays = (sum(item.getAvg() for item in macdCurrentHours) / len(macdCurrentHours) -
            sum(item.getAvg() for item in macdCurrentDays) / len(macdCurrentDays))
        self.macdCurrentMiddle = (sum(item.getAvg() for item in macdCurrentDays) / len(macdCurrentDays) -
            sum(item.getAvg() for item in macdCurrentMiddle) / len(macdCurrentMiddle))
        self.macdCurrentLong = (sum(item.getAvg() for item in macdCurrentMiddle) / len(macdCurrentMiddle) -
            sum(item.getAvg() for item in macdCurrentLong) / len(macdCurrentLong))

@dataclass
class PreparedData:
    time: int
    price: float
    macdCurrentHours: float
    macdCurrentDays: float
    macdCurrentMiddle: float
    macdCurrentLong: float
    volume: float
    avgOpenNext: float
    avgCloseNext: float
    avgMaxNext: float
    avgMinNext: float
    avgPriceNext: float

    def __init__(self, time: int,
        price: float,
        macdCurrentHours: float,
        macdCurrentDays: float,
        macdCurrentMiddle: float,
        macdCurrentLong: float,
        volume: float,
        avgOpenNext: float,
        avgCloseNext: float,
        avgMaxNext: float,
        avgMinNext: float,
        avgPriceNext: float):
            self.time = time
            self.price = price
            self.macdCurrentHours = macdCurrentHours
            self.macdCurrentDays = macdCurrentDays
            self.macdCurrentMiddle = macdCurrentMiddle
            self.macdCurrentLong = macdCurrentLong
            self.volume = volume
            self.avgOpenNext = avgOpenNext
            self.avgCloseNext = avgCloseNext
            self.avgMaxNext = avgMaxNext
            self.avgMinNext = avgMinNext
            self.avgPriceNext = avgPriceNext

    def create(current: DirtData, 
                 prev: DirtData, 
                 macdCurrentHours: list[DirtData],
                 macdCurrentDays: list[DirtData], 
                 macdCurrentMiddle: list[DirtData], 
                 macdCurrentLong: list[DirtData],
                 nextData: list[DirtData]):
        temNewVal = MiddleData(current, prev, macdCurrentHours, macdCurrentDays, macdCurrentMiddle, macdCurrentLong)
        
        time = temNewVal.time
        volume = temNewVal.volume
        price = temNewVal.price
        macdCurrentHours = temNewVal.macdCurrentHours
        macdCurrentDays = temNewVal.macdCurrentDays
        macdCurrentMiddle = temNewVal.macdCurrentMiddle
        macdCurrentLong = temNewVal.macdCurrentLong
        avgOpenNext = current.openPrice - sum(item.openPrice for item in nextData) / len(nextData)  
        avgCloseNext = current.closePrice - sum(item.closePrice for item in nextData) / len(nextData)
        avgMaxNext = current.maxPrice - max(item.maxPrice for item in nextData)
        avgMinNext = current.minPrice - min(item.minPrice for item in nextData)
        avgPriceNext = current.closePrice - sum(item.closePrice for item in nextData) / len(nextData)
        

        return PreparedData(time,
            price,
            macdCurrentHours,
            macdCurrentDays,
            macdCurrentMiddle,
            macdCurrentLong,
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
            "macdCurrentHours": self.macdCurrentHours,
            "macdCurrentDays": self.macdCurrentDays,
            "macdCurrentMiddle": self.macdCurrentMiddle,
            "macdCurrentLong": self.macdCurrentLong,
            "volume": self.volume,
            "avgOpenNext": self.avgOpenNext,
            "avgCloseNext": self.avgCloseNext,
            "avgMaxNext": self.avgMaxNext,
            "avgMinNext": self.avgMinNext,
            "avgPriceNext": self.avgPriceNext
        }
class Dirrection(Enum):
    Red = 1
    Green = 2
class BuyType(Enum):
    Hold = 1
    Long = 2
    Short = 3

class Recomendation:
    buyType: BuyType
    maxPrice: float
    minPrice: float
    openPrice: float
    closePrice: float
    avgPrice: float
    diffProcent: float
    sl: float
    tp: float
    diffBenefit: float
    diffLose: float
    direction: Dirrection
    slMax: float
    tpMax: float
    diffSlMax: float
    diffTpMax: float
    def __init__(self,lastCandle: DirtData, params):
        currentAvg = lastCandle.closePrice
        self.openPrice = lastCandle.openPrice - params[0]
        self.closePrice = lastCandle.closePrice - params[1]
        self.maxPrice = lastCandle.maxPrice - params[2]
        self.minPrice = lastCandle.minPrice - params[3]
        self.avgPrice = currentAvg - params[4]
        self.buyType = BuyType.Long if self.avgPrice > currentAvg else BuyType.Short
        self.diffProcent = abs(100 - self.avgPrice * 100 / currentAvg)
        self.tp = min([self.openPrice, self.closePrice]) if self.buyType == BuyType.Short else max([self.openPrice, self.closePrice])
        self.sl = max([self.openPrice, self.closePrice]) if self.buyType == BuyType.Short else min([self.openPrice, self.closePrice])
        self.diffBenefit = abs(100 - self.tp * 100 / currentAvg)
        self.diffLose = abs(100 - self.sl * 100 / currentAvg)
        self.direction = Dirrection.Red if self.closePrice < self.openPrice else Dirrection.Green
        
        self.tpMax = min([self.minPrice, self.maxPrice]) if self.buyType == BuyType.Short else max([self.minPrice, self.maxPrice])
        self.slMax = max([self.minPrice, self.maxPrice]) if self.buyType == BuyType.Short else min([self.minPrice, self.maxPrice])
        self.diffSlMax = abs(100 - self.tpMax * 100 / currentAvg)
        self.diffTpMax = abs(100 - self.slMax * 100 / currentAvg)

        self.buyType = BuyType.Hold if (
                (self.buyType == BuyType.Short and self.direction == Dirrection.Green) or
                (self.buyType == BuyType.Long and self.direction == Dirrection.Red) or
                (self.avgPrice > self.sl and self.avgPrice > self.tp) or
                (self.avgPrice < self.sl and self.avgPrice < self.tp) or
                (currentAvg > self.sl and self.buyType == BuyType.Short and currentAvg > self.tp and currentAvg < self.slMax) or
                (currentAvg < self.sl and self.buyType == BuyType.Long and currentAvg < self.tp and currentAvg > self.slMax)
            ) else self.buyType
