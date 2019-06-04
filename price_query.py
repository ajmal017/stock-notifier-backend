from alpha_vantage.timeseries import TimeSeries
import sys
import json

def curr_price_query(stocks, k):
    ts = TimeSeries(key=k)
    stock_dict = {}
    for stock in stocks:
        try:
            data, metadata = ts.get_intraday(symbol=stock, interval="1min", outputsize="compact")
            stock_dict[stock] = list(data.values())[0]["1. open"]
        except Exception as e:
            print(e)
            print(stock)
    print(stock_dict)
    return stock_dict

if __name__ == "__main__":
    stocks = sys.argv[1:]
    curr_price_query(stocks)
