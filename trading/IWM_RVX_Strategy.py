# Import yfinance
import matplotlib.pyplot as plt
import yfinance as yf
import quandl
import numpy as np
from pandas.plotting import register_matplotlib_converters

import Utils
from StdDevLimitOrder import portfolio


register_matplotlib_converters()


def runBackTest(start_date, end_date):
    pass


if __name__ == "__main__":
    # start_date = "2008-08-01"
    # end_date = "2009-09-06"

    start_date = "2016-01-01"
    end_date = "2019-01-01"

    # start_date = "2019-01-01"
    # end_date = "2020-06-11"

    timeStep = 1  # days

    spyData = Utils.getTickerData("IWM", start_date, end_date)
    vixData = Utils.getRVXData(start_date, end_date)

    spyClose = spyData.Close.to_numpy()
    vixClose = vixData['Close'].values
    vixAxes = vixData['Date']

    num = spyClose.shape[0]
    vixLen = vixClose.shape[0]
    print ("spyLen: ", num, ". vixLen:", vixLen)

    spyChangePercent = np.zeros(num)
    vixChangePercent = np.ones(vixLen)
    print "start_date: ", start_date, ". end_date: ", end_date
    print "timestep: ", timeStep, " days."
    for i in range(timeStep, num):
        spyChangePercent[i] = (
            spyClose[i]-spyClose[i-timeStep])/spyClose[i-timeStep]*100.0
    for i in range(timeStep, vixLen):
        vixChangePercent[i] = (
            vixClose[i]-vixClose[i-timeStep])/vixClose[i-timeStep]*100.0

    bothDropping = []
    bothRising = []
    for i in range(1, num-1):
        # if abs(spyChangePercent[i]) < 0.2:
        #     continue
        if(spyChangePercent[i] > 0.0 and vixChangePercent[i] > 0.0):
            bothRising += [i]
        if(spyChangePercent[i] < 0.0 and vixChangePercent[i] < 0.0):
            bothDropping += [i]

    acct = portfolio()
    transaction_dates = [spyData.axes[0][0]]
    portfolio = [spyClose[0]]
    cost_basis = []
    for i in range(timeStep, num):
        if i in bothDropping:
            cost_basis += [spyClose[i]]
        elif i in bothRising:
            if len(cost_basis) == 0:
                continue
            avg_cost = sum(cost_basis)/len(cost_basis)
            portfolio += [((spyClose[i] - avg_cost) /
                           avg_cost+1.0)*portfolio[-1]]
            transaction_dates += [spyData.axes[0][i]]
            cost_basis = []

    # print portfolio
    wins = 0.0
    for i in range(1, len(transaction_dates)):
        if(portfolio[i] < portfolio[i-1]):
            wins += 1
    print "winning rate: ", (1.0-wins/len(portfolio))*100.0
    print "Portfolio end value: ", portfolio[-1]
    print "Related Index fund: ", spyClose[-1]
    if(portfolio[-1] < spyClose[-1]):
        print "!!!!!!!!!!!!!! You failed to beat the market !!!!!!!!!!!!"
    else:
        print "~~~~~~~~~~~~~~~ You BEAT the market ~~~~~~~~~~~~~~~"

    plt.figure(figsize=[12, 8])
    plt.plot(vixAxes, vixClose, "-", label="RVX")
    plt.plot(spyData.axes[0], spyClose, "-", label="IWM")
    plt.legend()

    plt.xticks(rotation=90)
    plt.grid()
    plt.legend(fancybox=True, framealpha=0.3, loc="best")
    plt.title("Daily Percentage")

    print "bothRising: ", len(bothRising), "bothDropping", len(bothDropping)
    fig, ax1 = plt.subplots(figsize=[12, 8])
    ax1.plot(spyData.axes[0], spyClose, label="IWM")
    ax1.plot(transaction_dates, portfolio, "g.-", label="acct")
    for i in range(1, len(transaction_dates)):
        if(portfolio[i] < portfolio[i-1]):
            ax1.plot(transaction_dates[i], portfolio[i], "r.")
    # plt.plot(tltData.axes[0], tltClose, label="TLT")
    # plt.plot(gldData.axes[0], gldClose, label="GLD")
    # plt.plot(vixAxes, vixData, '.', label="VIX")
    for i in bothDropping:
        ax1.plot(spyData.axes[0][i], spyClose[i], "g*")
    for i in bothRising:
        ax1.plot(spyData.axes[0][i], spyClose[i], "r*")
    ax1.plot(spyData.axes[0][bothDropping[-1]],
             spyClose[bothDropping[-1]], "g*", label="buy, both Dropping")
    ax1.plot(spyData.axes[0][bothRising[-1]],
             spyClose[bothRising[-1]], "r*", label="sell, both Rising")
    plt.title("timeStep: " + str(timeStep) + " days")
    plt.xticks(rotation=0)
    plt.grid()
    plt.legend(fancybox=True, framealpha=0.3, loc="best")

    plt.show()
