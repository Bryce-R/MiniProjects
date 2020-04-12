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
end_date = "2020-04-11"

# plt.subplot(211)
# https://docs.quandl.com/docs/python-time-series
# pandas.core.frame.DataFrame
vix = quandl.get("CHRIS/CBOE_VX1.4", start_date=start_date,
                 end_date=end_date)
# vix.plot()
# print vix.values
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
# print spyPrice
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
sqrtDays = np.sqrt(252)
plt.figure()
plt.plot(spyChangePercent, 'g--+', label="spyChange")
plt.plot(spyChangeHigh, "b-", label="spyChangeHigh")
plt.plot(spyChangeLow, "r--+", label="spyChangeLow")
plt.plot(vixVal/sqrtDays, "--", label="vix-IV")
plt.plot(-vixVal/sqrtDays, "--", label="vix-IV")
plt.grid()
plt.legend(fancybox=True, framealpha=0.3, loc="best")
plt.show()
