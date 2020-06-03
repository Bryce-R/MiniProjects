import yfinance as yf


def getTickerData(ticker, start_date, end_date):
    ticker_data = yf.download(ticker, start_date, end_date)

    return ticker_data


if __name__ == "__main__":
    pass
