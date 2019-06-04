#import urllib2
#from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import first_time
import time

chrome_options = Options()

chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--disable-setuid-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")

def getStockData(symbols):
#    problems = open("not_working.txt", "w")
    stockData = {}
    y = 0
    driver = webdriver.Chrome(chrome_options=chrome_options)
    for sym in symbols:
        y += 1
        if y == 10:
            driver = webdriver.Chrome(executable_path='./chromedriver.exe', chrome_options=chrome_options)
            y = 0
        print(sym)
        url = "https://www.stockconsultant.com/consultnow/basicplus.cgi?symbol=" + sym
        supports = []
        resistances = []

        try:
            driver.get(url)
        except Exception:
            print("Error: cannot pull webpage of " + sym)
            continue

        #print(url)

        for x in range(8, 17):
            try:
                ele_string = "/html/body/div[@class='containerborder']/div[20]/div["+str(x)+"]"
                ele = driver.find_element_by_xpath(ele_string)
                text = ele.text
            except Exception:
                print("Error on "+str(x)+" on ticker "+sym)
#                problems.write(sym+"\n")
                break
                
            if len(text) > 0 and text[0] == '-':
                supports.append(text)
            elif len(text) > 0 and text[0] == '+':
                resistances.append(text)


        if len(supports) is 0  and len(resistances) is 0:
            continue;
                
        supnums = []
        resnums = []

        for sup in supports:
            supnums.append(sup.split()[2])
        for res in resistances:
            resnums.append(res.split()[2])

        supstrength = []
        resstrength = []

        for sup in supports:
            supstrength.append(sup.split()[-1])
        for res in resistances:
            resstrength.append(res.split()[-1])

        sups = []
        ress = []
        for sup in supports:
            sups.append((sup.split()[2], sup.split()[-1]))
        for res in resistances:
            ress.append((res.split()[2], res.split()[-1]))
        
        stockData[sym] = {"Supports" : sups, "Resistances" : ress}

    driver.close()
    driver.quit()
    return stockData

"""
test_page = 'https://www.stockconsultant.com/consultnow/basicplus.cgi?symbol=AMD'
html_page = urllib2.urlopen(test_page)
beaut_soup = BeautifulSoup(html_page, 'html.parser')
"""

if __name__ == "__main__":
    data = getStockData(first_time.tickers)
    print(data)
