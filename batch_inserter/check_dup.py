import database

def check():
    syms = [s['symbol'] for s in database.getTickers()]
    sset = set([i for i in syms if syms.count(i)> 1])
    print(sset)
    print(len(sset))
    for s in sset:
        database.deleteTicker(s)

if __name__ == "__main__":
    check()
