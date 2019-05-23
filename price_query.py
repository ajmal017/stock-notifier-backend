from alpha_vantage.timeseries import TimeSeries
import sys
import json

def curr_price_query(stocks):
    ts = TimeSeries(key="H3YZEN6PT1LGBV6U")
    stock_dict = {}
    for stock in stocks:
        data, metadata = ts.get_intraday(symbol=stock, interval="1min", outputsize="compact")
        print(list(data.values())[0]["1. open"])
        stock_dict[stock] = list(data.values())[0]["1. open"]
    print(stock_dict)
    return stock_dict

if __name__ == "__main__":
    stocks = sys.argv[1:]
    curr_price_query(stocks)