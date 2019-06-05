import sys
sys.path.append("..")
import first_time
import database
import price_query
import scraper
import time
import keys
import datetime as dt

def update_db():
    currently_in = database.getTickers()
    to_update = [s['symbol'] for s in currently_in]
    
    index = 0
    length = len(to_update)
    while index < length:
        end = index + 30
        if end > length:
            end = length
        current = to_update[index:end]
        print("Going to update "+str(current))
        sup_res = scraper.getStockData(current)

        updated = []
        for sym in current:
            if sym not in sup_res:
                continue
            database.updateSupports(sym, sup_res[sym]['Supports'])
            database.updateResistances(sym, sup_res[sym]['Resistances'])
            updated.append(sym)

        print("Updated "+str(updated))
        index = index + 30


if __name__ == "__main__":
    update_db()
