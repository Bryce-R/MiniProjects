# Import yfinance
import matplotlib.pyplot as plt
import yfinance as yf
import quandl
import numpy as np

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

quandl.ApiConfig.api_key = "Dne4SGor1UQsBqsyGP3X"

# plt.style.use('Solarize_Light2')

start_date = "2020-03-01"
end_date = "2020-04-10"

# plt.subplot(211)
# https://docs.quandl.com/docs/python-time-series
# pandas.core.frame.DataFrame
vix = quandl.get("CHRIS/CBOE_VX1.4", start_date=start_date,
                 end_date=end_date)
# vix.plot()
# print vix.axes
vixVal = vix.values
# Need subscription or premium API
# spy = quandl.get("EOD/SPY.4", start_date=start_date,
#                  end_date=end_date)
# spy.plot()
# vix = quandl.get("CHRIS/CBOE_VX1.4", start_date=start_date,
#                  end_date=end_date,  returns="numpy")
# plt.figure()
# print vix
# plt.plot(vix[:, 0], vix[:, 1], label="vix")


spyPrice = yf.download('SPY', start_date, end_date)
print spyPrice.axes[0]
# plt.subplot(212)
# spyPrice.Close.plot()
# plt.grid()
# plt.legend()


# plt.show()
spyClose = spyPrice.Close.to_numpy()
spyHigh = spyPrice.High.to_numpy()
spyLow = spyPrice.Low.to_numpy()
spyChangePercent = np.zeros(spyClose.shape[0])
spyChangeHigh = np.zeros(spyClose.shape[0])
spyChangeLow = np.zeros(spyClose.shape[0])
for i in range(1, spyClose.shape[0]):
    spyChangePercent[i] = (spyClose[i]-spyClose[i-1])/spyClose[i-1]*100.0
    spyChangeHigh[i] = (spyHigh[i]-spyClose[i-1])/spyClose[i-1]*100.0
    spyChangeLow[i] = (spyLow[i]-spyClose[i-1])/spyClose[i-1]*100.0


# print spyNp
sqrtDays = np.sqrt(252)
plt.figure(figsize=[12, 8])
plt.plot(spyPrice.axes[0], spyChangePercent, 'k', label="spyChange")
plt.plot(spyPrice.axes[0], spyChangeHigh, "go", label="spyChangeHigh")
plt.plot(spyPrice.axes[0], spyChangeLow, "ro", label="spyChangeLow")
for i in range(spyClose.shape[0]):
    plt.plot([spyPrice.axes[0][i], spyPrice.axes[0][i], spyPrice.axes[0][i]], [
             spyChangeHigh[i], spyChangePercent[i], spyChangeLow[i]], "b-")
plt.plot(vix.axes[0], vixVal/sqrtDays, "--", label="vix-IV")
plt.plot(vix.axes[0], -vixVal/sqrtDays, "--", label="vix-IV")
plt.xticks(rotation=0)
plt.grid()
plt.legend(fancybox=True, framealpha=0.3, loc="best")
plt.show()
