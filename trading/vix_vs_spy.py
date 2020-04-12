# Import yfinance
import matplotlib.pyplot as plt
import yfinance as yf
import quandl
import numpy as np

quandl.ApiConfig.api_key = "Dne4SGor1UQsBqsyGP3X"

start_date = "2020-01-01"
end_date = "2020-04-11"

# plt.subplot(211)
# https://docs.quandl.com/docs/python-time-series
# pandas.core.frame.DataFrame
vix = quandl.get("CHRIS/CBOE_VX1.4", start_date=start_date,
                 end_date=end_date)
# vix.plot()
# print vix.values
# Need subscription or premium API
# spy = quandl.get("EOD/SPY.4", start_date=start_date,
#                  end_date=end_date)
# spy.plot()
# vix = quandl.get("CHRIS/CBOE_VX1.4", start_date=start_date,
#                  end_date=end_date,  returns="numpy")
# plt.figure()
# print vix
# plt.plot(vix[:, 0], vix[:, 1], label="vix")


spyPrice = yf.download('SPY', '2020-01-01', '2020-04-11')
print spyPrice
# plt.subplot(212)
# spyPrice.Close.plot()
# plt.grid("on")
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
plt.figure()
plt.plot(spyChangePercent, label="spyChange")
plt.plot(spyChangeHigh, label="spyChangeHigh")
plt.plot(spyChangeLow, label="spyChangeLow")
plt.plot(vix/16.0, "--", label="vix/16")
plt.plot(-vix/16.0, "--", label="vix/16")
plt.grid("on")
plt.legend(fancybox=True, framealpha=0.3, loc="best")
plt.show()
