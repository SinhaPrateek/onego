from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import os
from datetime import datetime
rootDir = os.getcwd()
import itertools
from selenium.webdriver.chrome.options import Options
# from torrequest import TorRequest
import time
# import requests
from stem import Signal
from stem.control import Controller
import math

airports_file = r'/home/xena/Desktop/prateek/oneGo/onego_poc1/files/airports.py'
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
selected_airports = ['DEL-New Delhi','BLR-Bangalore', 'BOM-Mumbai','MAA-Chennai']


t_per_call = 33.2           # sec 
n_airports = len(selected_airports)
n_calls = math.factorial(n_airports)/math.factorial(n_airports-2)
total_time_expected = n_calls*t_per_call/(60*60)
print("total_time expected in hours: {}".format(total_time_expected))


# url = "https://paytm.com/flights/flightSearch/AGR-Agra/AGX-Agatti Island/1/0/0/E/2019-05-30"
# url = "https://paytm.com/flights/flightSearch/BLR-Bengaluru/BOM-Mumbai/1/0/0/E/2019-09-01"
data = pd.DataFrame(columns=['RecordDate', 'Airline','Flight','Dept_Date','Dept_Time', 'Origin', 'Duration','Stops','Arr_Date', 'Arr_Time', 'Destination', 'Total_Fare'])
files_dir = '/home/xena/Desktop/prateek/oneGo/onego_poc1/files/scraped_data'
filename = 'paytm_flights_second.csv'
data.to_csv(files_dir+'/'+ filename, mode='a', index=False)
DepDate = "2019-09-01"

def scrape_and_save(url):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome('/home/xena/Desktop/prateek/oneGo/onego_poc1/files/chromedriver', options=chrome_options)
    driver.implicitly_wait(30)
    driver.get(url)

    div_elem = driver.find_elements_by_css_selector('._3215.row')
    
    RecordDate = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    ArrDate ="NA"
    rows=[]
    for elem in div_elem:
        row = elem.text.split("\n")   # list of values
        row=row[:-3]                  # discard last three elements
        row.insert(0,RecordDate)
        row.insert(3,DepDate)
        row.insert(8,ArrDate)
        rows.append(row)

    data = pd.DataFrame(rows)
    
    data.to_csv(files_dir+'/' + filename, mode='a', index=False, header = False)
        
def renew_tor_ip():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(password="birth@1992")
        controller.signal(Signal.NEWNYM)        
        
t1 = time.time()
cnt = 0
for pair in itertools.permutations(selected_airports,2):
    if cnt > 10:
        break
# ### proxy using tor: approach 1 : for one call, it takes 0.73 min, so for 17556 calls, it would take 9 days
#     tr=TorRequest(password='birth@1992')  
#     tr.reset_identity() #Reset Tor
#     response= tr.get('http://ipecho.net/plain')
#     print ("New Ip Address",response.text)

# ### proxy using tor: approach 1 : for one call, it takes 33.2 sec, so for 17556 calls, it would take 6.75 days
    if cnt%10 == 0:
        renew_tor_ip()
    origin = pair[0]
    destination = pair[1]
    url = "https://paytm.com/flights/flightSearch/%s/%s/1/0/0/E/%s" % (origin, destination, DepDate)
    scrape_and_save(url)
    cnt=cnt+1
    print(url)

print("count of calls:{}".format(cnt))
#print("count of rows:{}".format(total_rows))
total_time = time.time() - t1
print("total time taken: {} sec".format(total_time)) 
print("total time taken: {} hours".format((total_time)/(60*60)))


