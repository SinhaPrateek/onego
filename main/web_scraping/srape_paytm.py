from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import os
from datetime import datetime
rootDir = os.getcwd()
import itertools

airports_file = r'C:\Self_Work\oneGo\onego_poc1\files\airports.py'
airports_dict = {}
indian_airports = []
foreign_airports = []
with open(airports_file) as f:  # using this code takes care of closing the file
    for line in f:
        airport_key = line.split(' = ')[0]
        airport_details = line.split(' = ')[1]
        airports_dict[airport_key] = eval(airport_details)

for value in airports_dict.values():
    if value.get('country') == 'India':
        indian_airport = "%s-%s" % (value.get('code'), value.get('city'))
        indian_airports.append(indian_airport)
    else:
        foreign_airport = "%s-%s" % (value.get('code'), value.get('city'))
        foreign_airports.append(foreign_airport)

print("indian_airports list size: %d" % len(indian_airports))
print("foreign_airports list size: %d" % len(foreign_airports))


# url = "https://paytm.com/flights/flightSearch/AGR-Agra/AGX-Agatti Island/1/0/0/E/2019-05-30"
# url = "https://paytm.com/flights/flightSearch/STV-Surat/TIR-Tirupati/1/0/0/E/2019-05-30"
data = pd.DataFrame(columns=['RecordDate', 'Airline','Flight','Dept_Date','Dept_Time', 'Origin', 'Duration','Stops','Arr_Date', 'Arr_Time', 'Destination', 'Total_Fare'])
files_dir = 'C:\\Self_Work\\oneGo\\onego_poc1\\files'
filename = 'paytm_flights.csv'
data.to_csv(files_dir+'\\'+ filename, mode='a', index=False)


def scrape_and_save(url):
    driver = webdriver.Chrome('C:/Self_Work/oneGo/onego_poc1/files/chromedriver')
    driver.implicitly_wait(30)
    driver.get(url)

    div_elem = driver.find_elements_by_css_selector('._3215.row')
    if len(div_elem)==0:
        RecordDate = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        DepDate = "2019-04-30"
        ArrDate ="NA"
        rows=[]
        for elem in div_elem:
            row = elem.text.split("\n")   # list of values
            row=row[:-3]              # discard last three elements
            row.insert(0,RecordDate)
            row.insert(3,DepDate)
            row.insert(8,ArrDate)
            rows.append(row)

        data = pd.DataFrame(rows,columns=['RecordDate','Airline','Flight','Dept_Date','Dept_Time','Origin','Duration','Stops','Arr_Date','Arr_Time','Destination','Total_Fare'])
        print(data.shape)
        data.to_csv(files_dir+'\\' + filename, mode='a', index=False, header = False)


cnt = 0
for pair in itertools.combinations(indian_airports,2):
    if cnt > 2:
        break
    origin = pair[0]
    destination = pair[1]
    url = "https://paytm.com/flights/flightSearch/%s/%s/1/0/0/E/2019-05-30" % (origin, destination)
    scrape_and_save(url)
    cnt=cnt+1
    print(url)
    print(cnt)



# import requests
# from lxml.html import fromstring
# def get_proxies():
#     url = 'https://free-proxy-list.net/'
#     response = requests.get(url)
#     parser = fromstring(response.text)
#     proxies = set()
#     for i in parser.xpath('//tbody/tr')[:10]:
#         if i.xpath('.//td[7][contains(text(),"yes")]'):
#             #Grabbing IP and corresponding PORT
#             proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
#             proxies.add(proxy)
#     return proxies
#
#
# proxies = get_proxies()
# print(proxies)
#
#
# PROXY = "165.22.57.60:8888" # IP:PORT or HOST:PORT
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--proxy-server=%s' % PROXY)
# chrome = webdriver.Chrome('C:/Self_Work/oneGo/onego_poc1/files/chromedriver',options=chrome_options))
#
#
# # chrome = webdriver.Chrome(options=chrome_options)
# chrome.get("http://whatismyipaddress.com")