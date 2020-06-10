# Import yfinance
import matplotlib.pyplot as plt
import yfinance as yf
import quandl
import numpy as np
import Utils

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


if __name__ == "__main__":
    start_date = "2008-08-01"
    end_date = "2009-09-06"
    # start_date = "2019-01-01"
    # end_date = "2020-06-06"
    print "start_date: ", start_date, ". end_date: ", end_date
    spyData = Utils.getTickerData("SPY", start_date, end_date)
    tltData = Utils.getTickerData("TLT", start_date, end_date)
    gldData = Utils.getTickerData("GLD", start_date, end_date)
    vixData = Utils.getVix(start_date, end_date)

    spyClose = spyData.Close.to_numpy()
    tltClose = tltData.Close.to_numpy()
    gldClose = gldData.Close.to_numpy()
    vixClose = vixData.values
    # print(vixClose)
    # print (vixData.axes[0])
    # print (spyData.axes[0])
    num = spyClose.shape[0]
    vixLen = vixClose.shape[0]
    print ("spyLen: ", num, ". vixLen:", vixLen)

    spyChangePercent = np.zeros(num)
    tltChangePercent = np.zeros(num)
    gldChangePercent = np.zeros(num)
    vixChangePercent = np.ones(vixLen)

    for i in range(1, num):
        spyChangePercent[i] = (spyClose[i]-spyClose[i-1])/spyClose[i-1]*100.0
        tltChangePercent[i] = (tltClose[i]-tltClose[i-1])/tltClose[i-1]*100.0
        gldChangePercent[i] = (gldClose[i]-gldClose[i-1])/gldClose[i-1]*100.0
    for i in range(1, vixLen):
        # prevClose = vixClose[i-1]
        # if(prevClose == 0.0) prevClose
        vixChangePercent[i] = (vixClose[i]-vixClose[i-1])/vixClose[i-1]*100.0

    plt.figure(figsize=[12, 8])
    # plt.plot(gldData.axes[0], gldChangePercent, ".", label="GLD")
    plt.plot(spyData.axes[0], spyChangePercent, ".-", label="SPY")
    # plt.plot(tltData.axes[0], tltChangePercent, ".", label="TLT")
    plt.plot(vixData.axes[0], vixChangePercent, '.-', label="VIX")

    # for i in range(1, vixLen):
    #     if(vixChangePercent[i] > 0.0):
    #         plt.plot(vixData.axes[0][i],
    #                  vixChangePercent[i], 'g.', )
    # for i in range(1, num):
    #     if(spyChangePercent[i] > 0.0):
    #         plt.plot(spyData.axes[0][i],
    #                  spyChangePercent[i], 'g+')
    bothDropping = []
    bothRising = []
    for i in range(1, num):
        if(spyChangePercent[i] > 0.0 and vixChangePercent[i] > 0.0):
            bothRising += [i]
        if(spyChangePercent[i] < 0.0 and vixChangePercent[i] < 0.0):
            bothDropping += [i]
            plt.plot([spyData.axes[0][i], vixData.axes[0][i]],
                     [spyChangePercent[i], vixChangePercent[i]], 'k.-')
    plt.xticks(rotation=90)
    plt.grid()
    plt.legend(fancybox=True, framealpha=0.3, loc="best")
    plt.title("Daily Percentage")

    print "bothRising: ", len(bothRising), "bothDropping", len(bothDropping)
    plt.figure(figsize=[12, 8])
    plt.plot(spyData.axes[0], spyClose, label="SPY")
    # plt.plot(tltData.axes[0], tltClose, label="TLT")
    # plt.plot(gldData.axes[0], gldClose, label="GLD")
    plt.plot(vixData.axes[0], vixData, '.', label="VIX")
    for i in bothDropping:
        plt.plot(spyData.axes[0][i], spyClose[i], "g*")
    for i in bothRising:
        plt.plot(spyData.axes[0][i], spyClose[i], "r*")
    plt.plot(spyData.axes[0][bothDropping[-1]],
             spyClose[bothDropping[-1]], "g*", label="buy, both Dropping")
    plt.plot(spyData.axes[0][bothRising[-1]],
             spyClose[bothRising[-1]], "r*", label="sell, both Rising")
    plt.xticks(rotation=0)
    plt.grid()
    plt.legend(fancybox=True, framealpha=0.3, loc="best")

    plt.show()
