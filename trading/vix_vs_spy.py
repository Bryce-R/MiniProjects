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


# spyPrice = yf.download('SPY', start_date, end_date)


# # plt.show()
# spyClose = spyPrice.Close.to_numpy()
# spyHigh = spyPrice.High.to_numpy()
# spyLow = spyPrice.Low.to_numpy()
# spyChangePercent = np.zeros(spyClose.shape[0])
# spyChangeHigh = np.zeros(spyClose.shape[0])
# spyChangeLow = np.zeros(spyClose.shape[0])
# for i in range(1, spyClose.shape[0]):
#     spyChangePercent[i] = (spyClose[i]-spyClose[i-1])/spyClose[i-1]*100.0
#     spyChangeHigh[i] = (spyHigh[i]-spyClose[i-1])/spyClose[i-1]*100.0
#     spyChangeLow[i] = (spyLow[i]-spyClose[i-1])/spyClose[i-1]*100.0


# # print spyNp
# sqrtDays = np.sqrt(252)
# plt.figure(figsize=[12, 8])
# plt.plot(spyPrice.axes[0], spyChangePercent, 'ko:', label="spyChange")
# plt.plot(spyPrice.axes[0], spyChangeHigh, "go", label="spyChangeHigh")
# plt.plot(spyPrice.axes[0], spyChangeLow, "ro", label="spyChangeLow")
# for i in range(spyClose.shape[0]):
#     plt.plot([spyPrice.axes[0][i], spyPrice.axes[0][i], spyPrice.axes[0][i]], [
#              spyChangeHigh[i], spyChangePercent[i], spyChangeLow[i]], "b-")

# plt.plot(vix.axes[0], vixVal/sqrtDays, "--", label="68%")
# plt.plot(vix.axes[0], -vixVal/sqrtDays, "--", label="68%")
# plt.plot(vix.axes[0], vixVal*2.0/sqrtDays, "--", label="95%")
# plt.plot(vix.axes[0], -vixVal*2.0/sqrtDays, "--", label="95%")
# plt.plot(vix.axes[0], vixVal*3.0/sqrtDays, "--", label="98%")
# plt.plot(vix.axes[0], -vixVal*3.0/sqrtDays, "--", label="98%")
# plt.xticks(rotation=0)
# plt.grid()
# plt.legend(fancybox=True, framealpha=0.3, loc="best")
# plt.show()
