from alpha_vantage.timeseries import TimeSeries
import sys
import json

"""
@param -- stocks, list of stock tickers
          k, key to be used for AlphaVantage
@return -- stock_dict, dictionary mapping stocks to their current price
"""
def curr_price_query(stocks, k):
    ts = TimeSeries(key=k)
    stock_dict = {}
    #for each stock, gets the prices using AlphaVantage's TimeSeries and then stores
    #the most recent stock price in stock_dict
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
