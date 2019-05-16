#import urllib2
#from bs4 import BeautifulSoup
from selenium import webdriver

symbols = ["AMD", "INTL", "AMZN", "AAPL", "NVDA"]

supports = []
resistances = []

for sym in symbols:
    driver = webdriver.Chrome("./chromedriver.exe")
    url = "https://www.stockconsultant.com/consultnow/basicplus.cgi?symbol=" + sym
    try:
        driver.get(url)
    except Exception:
        print("Error: cannot pull webpage of " + sym)



    for x in range(8, 17):
        ele_string = "/html/body/div[@class='containerborder'][8]/div[" + str(x) + "]"
        ele = driver.find_element_by_xpath(ele_string)
        text = ele.text
        print(text)
        if len(text) > 0 and text[0] == '-':
            supports.append(text)
        elif len(text) > 0 and text[0] == '+':
            resistances.append(text)

    driver.close()
    driver.quit()

for sup in supports:
    print(sup)
for res in resistances:
    print(res)

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

print("support nums")
for sup in supnums:
    print(sup)
print("strength nums")
for sup in supstrength:
    print(sup)


"""
test_page = 'https://www.stockconsultant.com/consultnow/basicplus.cgi?symbol=AMD'
html_page = urllib2.urlopen(test_page)
beaut_soup = BeautifulSoup(html_page, 'html.parser')
"""
