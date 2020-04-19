# Import yfinance
import matplotlib.pyplot as plt
import yfinance as yf
import quandl
import numpy as np

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
    plotVixVxSpy("2007-04-30", "2009-12-31")
    plt.show()
