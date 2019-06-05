import sys
import ast
sys.path.append("..")
import database
import time
import price_query
import keys
import datetime

def should_eval():
    open_time = datetime.time(13,30)
    close_time = datetime.time(20,00)
    current_time = datetime.datetime.utcnow().time()
    return current_time > open_time and current_time < close_time

def get_devices_for_sym(sym):
    device_sessions = []
    users = database.getUsersForTicker(sym)
    for u in users:
        sessions = database.getSessionsFromUser(u)
        for s in sessions:
            device_sessions.append((s['device'], s['k']))
    return list(set(device_sessions))

def poll_tickers_and_push(syms):
    print("Checking symbols "+str(syms))
    sup_res_dict = {}
    for sym in syms:
        supports = database.getSupportsForTicker(sym)
        s_tuples = []
        for sup in supports:
            sup_val = float(sup[0])
            s_tuples.append((sup_val + sup_val*.01, sup_val, sup[1]))
        s_tuples.sort(key = lambda x: x[0])
        
        resistances = database.getResistancesForTicker(sym)
        r_tuples = []
        for res in resistances:
            res_val = float(res[0])
            r_tuples.append((res_val - res_val*.01, res_val, res[1]))
        r_tuples.sort(key = lambda x: x[0], reverse=True)

        sup_res_dict[sym] = (s_tuples, r_tuples)

    print("S/R info: "+str(sup_res_dict))
    
    npk = 0
    ki = 0
    while should_eval():
        start_time = int(time.time())
        next_time = start_time + 300
        
        
        for sym in syms:
            try:
                print(sym)
                price = price_query.curr_price_query([sym], keys.price_keys[ki])
                npk = npk+1
                if npk == 5:
                    ki = ki + 1
                    if ki == len(keys.price_keys):
                        ki = 0
                        
                if len(price) == 0:
                    print("Was unable to pull price for "+sym+" at time "+str(datetime.datetime.utcnow().time()))
                    continue
                price_amt = float(price[sym])
                print("Current price is "+str(price_amt))
                for s in sup_res_dict[sym][0]:
                    if price_amt < s[0] and price_amt < s[1]:
                        # Notification framework
                        print("Symbol "+sym+" has broken support "+str(s[1])+" of strength "+str(s[2])+" and is currently at "+str(price_amt))
                        break
                    elif price_amt < s[0] and price_amt > s[1]:
                        # Notification framework
                        print("Symbol "+sym+" is reaching support "+str(s[1])+" of strength "+str(s[2])+" and is currently at "+str(price_amt))
                        break
                    
                for r in sup_res_dict[sym][1]:
                    if price_amt > r[0] and price_amt > r[1]:
                        # Notification framework
                        print("Symbol "+sym+" has broken resistance "+str(r[1])+" of strength "+str(r[2])+" and is currently at "+str(price_amt))
                        break
                    elif price_amt > r[0] and price_amt < r[1]:
                        # Notification framework
                        print("Symbol "+sym+" is reaching resistance "+str(r[1])+" of strength "+str(r[2])+" and is currently at "+str(price_amt))
                        break
                    
                devices = get_devices_for_sym(sym)
            except Exception as e:
                print("An exception for "+sym+" was caught at "+str(datetime.datetime.utcnow().time())+": "+str(e))

        current_time = int(time.time())
        if current_time < next_time:
            sleep_amt = next_time - current_time
            print("Sleeping for "+str(sleep_amt)+" seconds")
            time.sleep(sleep_amt)
            


if __name__ == "__main__":
    supported_tickers = [s['symbol'] for s in database.getTickers()]
    if len(sys.argv) == 1:
        print("Not enough arguments")
    elif len(sys.argv) == 2:
        tickers = ast.literal_eval(sys.argv[1])
        if type(tickers) is list:
            tickers = list(set(tickers))
            sup_tickers_set = set(supported_tickers)
            available_tickers = [sym for sym in tickers if sym in sup_tickers_set]
            poll_tickers_and_push(available_tickers)
        else:
            print("One argument given but not a list")
    elif len(sys.argv) == 3:
        begin = ast.literal_eval(sys.argv[1])
        end = ast.literal_eval(sys.argv[2])
        if type(begin) is not int or type(end) is not int:
            print("Two arguments given but at least one is not an int")
        elif begin < 0 or end > len(supported_tickers):
            print("Two ints given but invalid ranges")
        else:
            poll_tickers_and_push(supported_tickers[begin:end])
