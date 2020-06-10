import yfinance as yf
import quandl

import datetime
import pandas as pd

quandl.ApiConfig.api_key = "Dne4SGor1UQsBqsyGP3X"


def formatDateTime(dateTime):
    return datetime.datetime.strptime(dateTime, '%Y-%m-%d').strftime('%m/%d/%y')


def getTickerData(ticker, start_date, end_date):
    ticker_data = yf.download(ticker, start_date, end_date)

    return ticker_data


def getVix(start_date, end_date):
    # plt.subplot(211)
    # https://docs.quandl.com/docs/python-time-series
    # pandas.core.frame.DataFrame
    vixData = quandl.get("CHRIS/CBOE_VX1.4", start_date=start_date,
                         end_date=end_date)

    return vixData


def getRVXData(start_date, end_date):
    startDate = formatDateTime(start_date)
    endDate = formatDateTime(end_date)
    data = pd.read_csv("rvxdailyprices.csv", skiprows=2)
    # print data.head()
    # print data.shape
    # print data.columns
    # print data['Date']

    data['Date'] = pd.to_datetime(data['Date'])
    mask = (data['Date'] > startDate) & (data['Date'] < endDate)
    # Date   Open   High    Low  Close
    return data[mask]


def getVixDataFromCSV(filename, start_date, end_date):
    startDate = formatDateTime(start_date)
    endDate = formatDateTime(end_date)
    data = pd.read_csv(filename, skiprows=1)
    print data.head()
    # print data.shape
    # print data.columns
    # print data['Date']

    data['Date'] = pd.to_datetime(data['Date'])
    mask = (data['Date'] > startDate) & (data['Date'] < endDate)
    # Date   Open   High    Low  Close
    return data[mask]


if __name__ == "__main__":
    pass
