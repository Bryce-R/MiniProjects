from verification import getSpyAndVix


import numpy as np
import matplotlib.pyplot as plt


def getVixIndicatedStd(vix, stdMultiple):
    sqrtDays = np.sqrt(252)
    return vix*stdMultiple/sqrtDays/100.0


if __name__ == "__main__":
    start_date = "2020-01-01"
    end_date = "2020-04-26"
    vixData, spyData = getSpyAndVix(start_date, end_date)

    vixValues = vixData.values
    vixAxes = vixData.axes[0]
    spyClose = spyData.Close.to_numpy()
    spyHigh = spyData.High.to_numpy()
    spyLow = spyData.Low.to_numpy()
    spyAxes = spyData.axes[0]
    spyPositive = np.ones(spyClose.shape[0])*spyClose[0]
    spyNegative = np.ones(spyClose.shape[0])*spyClose[0]

    n = spyClose.shape[0]
    stdMultiple = 1.0

    print "Using date from ", start_date, " to ", end_date
    print "Using standard deviation multiple of ", stdMultiple
    for i in range(1, n):
        vixIndex = min(i-1, len(vixValues) - 1)
        spyPositive[i] = spyClose[i-1] * \
            (1.0 + getVixIndicatedStd(vixValues[vixIndex], stdMultiple))
        spyNegative[i] = spyClose[i-1] * \
            (1.0 - getVixIndicatedStd(vixValues[vixIndex], stdMultiple))

    plt.figure(figsize=[12, 8])
    plt.plot(spyAxes, spyHigh, "go", label="spyHigh")
    plt.plot(spyAxes, spyPositive, "gv", label="spyStd+")
    plt.plot(spyAxes, spyClose, "b-o", label="spyClose")
    plt.plot(spyAxes, spyNegative, "r^", label="spyStd-")
    plt.plot(spyAxes, spyLow, "ro", label="spyLow")
    for i in range(n):
        plt.plot([spyAxes[i], spyAxes[i]], [
            spyPositive[i], spyNegative[i]], "c--")
        if spyHigh[i] >= spyPositive[i] or spyLow[i] <= spyNegative[i]:
            plt.plot([spyAxes[i], spyAxes[i], spyAxes[i]], [
                spyHigh[i], spyClose[i], spyLow[i]], "k-")

    plt.xticks(rotation=0)
    plt.grid()
    plt.legend(fancybox=True, framealpha=0.3, loc="best")
    plt.show()
