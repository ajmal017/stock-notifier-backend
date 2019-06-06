import sys
sys.path.append("..")
import scraper
import database
import ast

def update_db(syms):
    
    index = 0
    length = len(syms)
    while index < length:
        end = index + 30
        if end > length:
            end = length
        current = syms[index:end]
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
    if len(sys.argv) == 1:
        currently_in = database.getTickers()
        to_update = [s['symbol'] for s in currently_in]
        update_db(to_update)
    else:
        tickers = ast.literal_eval(sys.argv[1])
        update_db(tickers)
