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
    # https://docs.quandl.com/docs/python-time-series
    # pandas.core.frame.DataFrame
    vix = quandl.get("CHRIS/CBOE_VX1.4", start_date=start_date,
                     end_date=end_date)
    fig, axes = plt.subplots(nrows=2, ncols=1, sharex=True)

    vix.plot(ax=axes[0])
    axes[0].grid()
    axes[0].set_ylabel("vix")
    spyPrice = yf.download('SPY', start_date, end_date)
    spyPrice.Close.plot(ax=axes[1])
    plt.grid()
    axes[1].set_ylabel("spy")


if __name__ == "__main__":
    # plotVixVxSpy("2020-03-01", "2020-04-10")

    # plotVixVxSpy("2008-09-01", "2009-12-01")

    # plotVixVxSpy("2008-12-01", "2009-03-10")
    # plotVixVxSpy("2008-03-10", "2009-05-10")
    plotVixVxSpy("2007-04-30", "2009-12-31")
    plt.show()
