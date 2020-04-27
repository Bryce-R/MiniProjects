# Import yfinance
import matplotlib.pyplot as plt
import yfinance as yf
import quandl
import numpy as np

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

quandl.ApiConfig.api_key = "Dne4SGor1UQsBqsyGP3X"
sqrtDays = np.sqrt(252)


class percent:
    def __init__(self):
        self.positive = 0.0
        self.negative = 0.0


def getSpyAndVix(start_date, end_date):
    print "From ", start_date, " to ", end_date
    # plt.subplot(211)
    # https://docs.quandl.com/docs/python-time-series
    # pandas.core.frame.DataFrame
    vixData = quandl.get("CHRIS/CBOE_VX1.4", start_date=start_date,
                         end_date=end_date)
    spyData = yf.download('SPY', start_date, end_date)

    return vixData, spyData


if __name__ == "__main__":
    start_date = "2020-01-01"
    end_date = "2020-04-26"
    vixData, spyData = getSpyAndVix(start_date, end_date)
    vixVal = vixData.values

    plt.show()

    # start_date = "2007-04-30"
    # end_date = "2009-12-31"

    # start_date = "2007-04-30"
    # end_date = "2020-04-09"

    # start_date = "2008-12-01"
    # end_date = "2009-03-10"

    # start_date = "2009-03-10"
    # end_date = "2009-05-10"

    # print vix.axes

    print len(vixVal)

    spyPrice = yf.download('SPY', start_date, end_date)

    # spxlData = yf.download('SPXL', start_date, end_date)
    # spxsData = yf.download('SPXS', start_date, end_date)

    # spxl = spxlData.Close.to_numpy()
    # spxs = spxsData.Close.to_numpy()

    spyClose = spyPrice.Close.to_numpy()
    spyHigh = spyPrice.High.to_numpy()
    spyLow = spyPrice.Low.to_numpy()
    spyChangePercent = np.zeros(spyClose.shape[0])
    spyChangeHigh = np.zeros(spyClose.shape[0])
    spyChangeLow = np.zeros(spyClose.shape[0])
    money = np.zeros(spyClose.shape[0])

    print spyClose.shape[0]

    for i in range(1, spyClose.shape[0]):
        spyChangePercent[i] = (spyClose[i]-spyClose[i-1])/spyClose[i-1]*100.0
        spyChangeHigh[i] = (spyHigh[i]-spyClose[i-1])/spyClose[i-1]*100.0
        spyChangeLow[i] = (spyLow[i]-spyClose[i-1])/spyClose[i-1]*100.0

    positive = 0.0
    negative = 0.0
    holdTilClose = percent()
    holdSometime = percent()
    stdMultiple = 1.0
    print "Using ", stdMultiple, " times of standard deviation."
    money[0] = 2500
    prevMoney = money[0]

    for i in range(1, spyClose.shape[0]):
        vixIndex = min(i-1, len(vixVal) - 1)
        if(spyChangePercent[i-1] >= vixVal[vixIndex]*stdMultiple/sqrtDays):
            num = int(prevMoney / spyClose[i-1])
            money[i] = prevMoney + (spyClose[i-1] - spyClose[i])*num
            prevMoney = money[i]
            if spyChangePercent[i] <= 0.0:
                holdTilClose.positive += 1.0
            else:
                holdTilClose.negative += 1.0
            if spyChangeLow[i] <= 0.0:
                holdSometime.positive += 1.0
            else:
                holdSometime.negative += 1.0
        elif (spyChangePercent[i-1] <= -vixVal[vixIndex]*stdMultiple/sqrtDays):
            num = int(prevMoney / spyClose[i-1])
            money[i] = prevMoney + (spyClose[i] - spyClose[i-1])*num
            prevMoney = money[i]
            if spyChangePercent[i] >= 0.0:
                holdTilClose.positive += 1.0
            else:
                holdTilClose.negative += 1.0
            if spyChangeHigh[i] >= 0.0:
                holdSometime.positive += 1.0
            else:
                holdSometime.negative += 1.0

    print "positive", holdTilClose.positive, ". Total: ", spyClose.shape[0]
    print ("Hold til Close: positive rate: ", holdTilClose.positive /
           (holdTilClose.positive + holdTilClose.negative)*100, "%.")
    print ("Hold sometime: positive rate: ", holdSometime.positive /
           (holdSometime.positive + holdSometime.negative)*100, "%.")

    print "Closing price of SPY: ", spyClose[-1]
    print "anticipated move percentage: ", (
        vixVal[-1]*stdMultiple/sqrtDays/100.0)[0]
    print "high:", spyClose[-1] * \
        (1.0 + vixVal[-1]*stdMultiple/sqrtDays/100.0)[0]
    print "low:", spyClose[-1]*(1.0 - vixVal[-1]*stdMultiple/sqrtDays/100.0)[0]

    plt.figure(figsize=[12, 8])
    plt.plot(spyPrice.axes[0], spyChangeHigh, "go", label="spyChangeHigh")
    plt.plot(spyPrice.axes[0], spyChangeLow, "ro", label="spyChangeLow")
    plt.plot(spyPrice.axes[0], spyChangePercent, 'ko:', label="spyChange")
    for i in range(spyClose.shape[0]):
        plt.plot([spyPrice.axes[0][i], spyPrice.axes[0][i], spyPrice.axes[0][i]], [
            spyChangeHigh[i], spyChangePercent[i], spyChangeLow[i]], "b-")
    plt.plot(vixData.axes[0], vixVal/sqrtDays, "--", label="68%")
    plt.plot(vixData.axes[0], -vixVal/sqrtDays, "--", label="68%")
    plt.plot(vixData.axes[0], vixVal*2.0/sqrtDays, "--", label="95%")
    plt.plot(vixData.axes[0], -vixVal*2.0/sqrtDays, "--", label="95%")
    plt.plot(vixData.axes[0], vixVal*3.0/sqrtDays, "--", label="98%")
    plt.plot(vixData.axes[0], -vixVal*3.0/sqrtDays, "--", label="98%")
    plt.xticks(rotation=0)
    plt.grid()
    plt.legend(fancybox=True, framealpha=0.3, loc="best")

    plt.figure(figsize=[12, 8])
    plt.plot(spyPrice.axes[0], money, 'ko:', label="acct")
    plt.xticks(rotation=0)
    plt.grid()
    plt.legend(fancybox=True, framealpha=0.3, loc="best")

    plt.show()
