from verification import getSpyAndVix


import numpy as np
import matplotlib.pyplot as plt


def getVixIndicatedPerc(vix, stdMultiple=1.0):
    sqrtDays = np.sqrt(252)
    return vix*stdMultiple/sqrtDays


def getVixIndicatedStd(vix, stdMultiple=1.0):
    return getVixIndicatedPerc(vix, stdMultiple)/100.0


if __name__ == "__main__":
    # start_date = "2020-01-01"
    # end_date = "2020-04-26"
    start_date = "2018-01-01"
    end_date = "2020-04-26"
    vixData, spyData = getSpyAndVix(start_date, end_date)

    vixValues = vixData.values
    vixAxes = vixData.axes[0]
    spyClose = spyData.Close.to_numpy()
    spyHigh = spyData.High.to_numpy()
    spyLow = spyData.Low.to_numpy()
    spyAxes = spyData.axes[0]

    n = spyClose.shape[0]

    spyChangePercent = np.zeros(n)
    spyChangeHigh = np.zeros(n)
    spyChangeLow = np.zeros(n)

    spyChangePercentOfVix = np.zeros(n)
    spyChangeHighOfVix = np.zeros(n)
    spyChangeLowOfVix = np.zeros(n)

    for i in range(1, n):
        vixIndex = min(i-1, len(vixValues) - 1)
        spyChangePercent[i] = (spyClose[i]-spyClose[i-1])/spyClose[i-1]*100.0
        spyChangeHigh[i] = (spyHigh[i]-spyClose[i-1])/spyClose[i-1]*100.0
        spyChangeLow[i] = (spyLow[i]-spyClose[i-1])/spyClose[i-1]*100.0
        vixPercent = getVixIndicatedPerc(vixValues[vixIndex])
        spyChangePercentOfVix[i] = spyChangePercent[i] / vixPercent
        spyChangeHighOfVix[i] = spyChangeHigh[i] / vixPercent
        spyChangeLowOfVix[i] = spyChangeLow[i] / vixPercent

    print "Using date from ", start_date, " to ", end_date

    plt.figure(figsize=[12, 8])
    plt.plot([0, 0], [-10, 10], "k-", zorder=1)
    plt.plot([-4, 4], [0, 0], "k-", zorder=1)
    plt.gca().fill_between([0, 3], 0, -10, alpha=0.3, color="grey")
    plt.gca().fill_between([0, -3], 0, 10, alpha=0.3, color="grey")
    for i in range(1, n-1):
        vixIndex = min(i-1, len(vixValues) - 1)
        if(abs(spyChangePercentOfVix[i]) > 1.0 and vixValues[vixIndex] > 30.0):
            plt.plot(spyChangePercentOfVix[i],
                     spyChangePercent[i+1], "bo", zorder=2)
            plt.plot(spyChangePercentOfVix[i],
                     spyChangeHigh[i+1], "gv")
            plt.plot(spyChangePercentOfVix[i],
                     spyChangeLow[i+1], "r^")
        # else:
        #     plt.plot(spyChangePercentOfVix[i],
        #              spyChangePercentOfVix[i+1], "b+")
    plt.xlabel("today, in terms of vix")
    plt.ylabel("tomorrow, percentage")
    plt.grid()
    plt.legend(fancybox=True, framealpha=0.3, loc="best")
    plt.show()
