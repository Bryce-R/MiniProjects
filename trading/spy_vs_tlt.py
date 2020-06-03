# Import yfinance
import matplotlib.pyplot as plt
import yfinance as yf
import quandl
import numpy as np
import Utils

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

quandl.ApiConfig.api_key = "Dne4SGor1UQsBqsyGP3X"


def plotVixVxSpy(start_date, end_date):
    print "plotting data from ", start_date, " to ", end_date
    fig, axes = plt.subplots(nrows=2, ncols=1, sharex=True)
    tltPrice = yf.download('TLT', start_date, end_date)
    tltPrice.Close.plot(ax=axes[0])
    axes[0].grid()
    axes[0].set_ylabel("TLT")
    spyPrice = yf.download('SPY', start_date, end_date)
    spyPrice.Close.plot(ax=axes[1])
    plt.grid()
    axes[1].set_ylabel("SPY")


if __name__ == "__main__":
    # plotVixVxSpy("2020-03-01", "2020-04-10")
    # plotVixVxSpy("2008-09-01", "2009-12-01")
    # plotVixVxSpy("2008-12-01", "2009-03-10")
    # plotVixVxSpy("2008-03-10", "2009-05-10")
    # plotVixVxSpy("2007-04-30", "2009-12-31")
    start_date = "2020-01-01"
    end_date = "2020-05-28"
    spyData = Utils.getTickerData("SPY", start_date, end_date)
    tltData = Utils.getTickerData("TLT", start_date, end_date)
    spyClose = spyData.Close.to_numpy()
    tltClose = tltData.Close.to_numpy()

    num = spyClose.shape[0]
    spyChangePercent = np.zeros(num)
    tltChangePercent = np.zeros(num)

    for i in range(1, num):
        spyChangePercent[i] = (spyClose[i]-spyClose[i-1])/spyClose[i-1]*100.0
        tltChangePercent[i] = (tltClose[i]-tltClose[i-1])/tltClose[i-1]*100.0
    plt.figure(figsize=[12, 8])
    plt.plot(spyData.axes[0], spyChangePercent, label="SPY")
    plt.plot(tltData.axes[0], tltChangePercent, label="TLT")
    for i in range(1, num):
        # print spyChangePercent[i], tltChangePercent[i],
        if spyChangePercent[i] > 0 and tltChangePercent[i] > 0.0:
            plt.plot([spyData.axes[0][i], tltData.axes[0][i]], [
                     spyChangePercent[i], tltChangePercent[i]], "g.-")
        if spyChangePercent[i] < 0 and tltChangePercent[i] < 0.0:
            plt.plot([spyData.axes[0][i], tltData.axes[0][i]], [
                     spyChangePercent[i], tltChangePercent[i]], "r.-")
    plt.xticks(rotation=0)
    plt.grid()
    plt.legend(fancybox=True, framealpha=0.3, loc="best")
    plt.show()
