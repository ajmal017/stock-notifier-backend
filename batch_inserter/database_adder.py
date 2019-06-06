import sys
sys.path.append("..")
import first_time
import database
import price_query
import scraper
import time
import datetime as dt
import ast
import os

def add_tickers(sym_list, names_list, price_keys):
    with open('not_working.txt') as f:
        lines = f.read().splitlines()
    both_list = list(zip(sym_list, names_list))
    currently_in = database.getTickers()
    todo = []
    for sym, name in both_list:
        if sym in lines:
            continue
        info = {'name': name, 'symbol': sym}
        if info in currently_in:
            continue
        todo.append((sym, name))

    index = 0
    length = len(todo)
    not_working = []
    t = dt.datetime.now()
    minute_count = 0 
    ki = 0
    while index < length:
        end = index + 5
        if end > length:
            end = length
        current = todo[index:end]
        syms, _ = zip(*current)
        print(syms)
        print(ki)
        sup_res = scraper.getStockData(syms)
        prices = {}
        while len(prices) == 0:
            try:
                print(ki)
                prices = price_query.curr_price_query(syms, price_keys[ki])                
            except Exception as e:
                print(e)
                time.sleep(10)
            finally:
                ki = ki + 1
                if ki == len(price_keys):
                    ki = 0
                    break
                    time.sleep(10)
        for s, n in current:
            if s not in sup_res or s not in prices:
                not_working.append(s)
                continue
            database.addTicker(s, n, sup_res[s]['Supports'], sup_res[s]['Resistances'], ['alden', 'brian'], last=prices[s])
        index = index + 5

    print(not_working)
    return not_working
        
if __name__ == "__main__":
    keys = ast.literal_eval(os.environ['ALPHA_VANTAGE_KEYS'])
    not_working = add_tickers(first_time.tickers, first_time.names, keys)
