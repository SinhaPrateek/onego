import json
import requests

# For more info on API - https://www.rome2rio.com/documentation/1-4/search/
# regrading using request library for querying through a url -https://2.python-requests.org//en/latest/user/quickstart/

api_token = 'bfOhgi4x'
api_url_base = 'http://free.rome2rio.com/api/1.4/json/Search'

origin_palce = 'delhi'
dest_place = 'patna'
origin_position = '28.646811,77.236252' # Jama Masjid, New Delhi
dest_position = '12.891430,77.606113' # Ayyappa Swami Temple, Vijaya Bank Layout

url_arguments_with_place_name = {'key':api_token,'oName':origin_palce,'dName':dest_place}
url_arguments_with_place_latlong = {'key':api_token,'oPos':origin_position,'dPos':dest_position}

def get_route_info():

    api_url = '{0}'.format(api_url_base)

    response = requests.get(api_url, params=url_arguments_with_place_latlong)
    #print(response.url)
    #print(response.status_code) - success code - 200, failure code - others (400 - for wrong formatted url)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None

route_info_json = get_route_info()
#print(route_info_json['routes'])

print("Places Array")
print(route_info_json['places'])
print("-----------------------")
print("Airlines")
print(route_info_json['airlines'])
print("-----------------------")
print("Aircrafts")
print(route_info_json['aircrafts'])
print("-----------------------")
print('Agencies Array')
print(route_info_json['agencies'])
print('------------------------')
print('Vehicles Array')
print(route_info_json['vehicles'])
print("------------------------")


print("Routes Data",'\n')
i = 0
for route_dict in route_info_json['routes']:
    i = i+1
    print("Route Number", i)
    for key,value in route_dict.items():
        if key!= 'segments':
            print(key,"-----",value)
        else:
            print(key,'--------')
            for segment in value:
                print('\t\t',segment)
                print('\t\t','-------')
    print("-----------------------------")
    print("-----------------------------")
