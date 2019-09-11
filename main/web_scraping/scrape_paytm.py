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
import argparse

if __name__ == "__main__":
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("--DepDate", type=str)
    parser.add_argument("--selected_file", type=str, default = 'selected_airports_50.txt')
    parser.add_argument("--output_file", type=str, default = 'paytm_flights_test.csv')
    args = parser.parse_args()
    
    

input_dir = "/home/xena/Desktop/prateek/oneGo/onego_poc1/files/" 
output_dir = "/home/xena/Desktop/prateek/oneGo/onego_poc1/files/scraped_data/" 
airports_file = input_dir + "airports.py"
selected_airports_file = input_dir + args.selected_file
selected_airports = set()
airports_dict = {}
indian_airports = []
selected_airports_code_name = []
foreign_airports = []

with open(selected_airports_file) as f:
    for line in f:
        selected_airports.add(line.split("\n")[0])

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

selected_airports_code_name = [airport for airport in indian_airports if airport.split('-')[0] in selected_airports]

print("indian_airports list size: %d" % len(indian_airports))
print("indian_airports_selected list size: %d" % len(selected_airports_code_name))
print("foreign_airports list size: %d" % len(foreign_airports))


t_per_call = 6.54
n_airports = len(selected_airports_code_name)
n_calls = math.factorial(n_airports)/math.factorial(n_airports-2)
total_time_expected = n_calls*t_per_call/(60*60)
print("total_time expected in hours: {}".format(total_time_expected))


# url = "https://paytm.com/flights/flightSearch/AGR-Agra/AGX-Agatti Island/1/0/0/E/2019-05-30"
# url = "https://paytm.com/flights/flightSearch/BLR-Bengaluru/BOM-Mumbai/1/0/0/E/2019-09-01"
data = pd.DataFrame(columns=['RecordDate', 'Airline','Flight','Dept_Date','Dept_Time', 'Origin', 'Duration','Stops','Arr_Date', 'Arr_Time', 'Destination', 'Total_Fare'])

# output_file = 'paytm_flights_test.csv'
data.to_csv(output_dir + args.output_file, mode='a', index=False)
DepDate = args.DepDate

def scrape_and_save(url,origin,destination):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome('/home/xena/Desktop/prateek/oneGo/onego_poc1/files/chromedriver', options=chrome_options)
    driver.implicitly_wait(10)
    driver.get(url)

    div_elem = driver.find_elements_by_css_selector('._3215.row')
    
        
    RecordDate = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    ArrDate ="NA"
    rows=[]
    if(len(div_elem) > 0):
        for elem in div_elem:
            row = elem.text.split("\n")   # list of values
            row=row[:-3]                  # discard last three elements
            row.insert(0,RecordDate)
            row.insert(3,DepDate)
            row.insert(8,ArrDate)
            rows.append(row)
    else:
       rows = [[RecordDate, 'NA','NA',DepDate,'NA', origin, 'NA','NA', ArrDate, 'NA', destination, 'NA']]

    data = pd.DataFrame(rows)
    
    data.to_csv(output_dir + args.output_file, mode='a', index=False, header = False)
        
def renew_tor_ip():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(password="birth@1992")
        controller.signal(Signal.NEWNYM)        
        
t1 = time.time()
cnt = 0
for pair in itertools.permutations(selected_airports_code_name,2):
#    if cnt > 1:
#        break
# ### proxy using tor: approach 1 : for one call, it takes 0.73 min, so for 17556 calls, it would take 9 days
#     tr=TorRequest(password='birth@1992')  
#     tr.reset_identity() #Reset Tor
#     response= tr.get('http://ipecho.net/plain')
#     print ("New Ip Address",response.text)

#### proxy using tor: approach 1 : for one call, it takes 33.2 sec, so for 17556 calls, it would take 6.75 days
#### For 35 airports,1190 calls(permutations), it took 4.5238 hrs that is 13.68 sec per call
#### For 50 airports,2450 calls(p), it took 8.849 hrs that is 13 sec per call
#### After latest optimization(implicit_wait(10sec)) , for 50 airports, 2450 calls, it took 6.86 hrs, 2 hrs lesser than before, 10.1 sec per call
    if cnt%10 == 0:
        #time_renew_first = time.time()
        renew_tor_ip()
        print(cnt)
        #time_renew = time.time() - time_renew_first
        #print("time_renew: {} sec".format(time_renew))
    origin = pair[0]
    destination = pair[1]
    url = "https://paytm.com/flights/flightSearch/%s/%s/1/0/0/E/%s" % (origin, destination, DepDate)
    scrape_and_save(url,origin,destination)
    cnt=cnt+1
    print(url)
    

print("count of calls:{}".format(cnt))
#print("count of rows:{}".format(total_rows))
total_time = time.time() - t1
# print("total time taken: {} sec".format(total_time)) 
print("total time taken: {} hours and completed at {}".format((total_time)/(60*60), time.time()))



