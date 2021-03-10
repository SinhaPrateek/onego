import json
import requests
import googlemaps

# For more info on API - https://www.rome2rio.com/documentation/1-4/search/
# regrading using request library for querying through a url -https://2.python-requests.org//en/latest/user/quickstart/
# python client for google maps services https://github.com/googlemaps/google-maps-services-python
# https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key=key

api_token = 'abcd'
api_url_base = 'http://free.rome2rio.com/api/1.4/json/Search'
api_url_base_auto_complete = 'http://free.rome2rio.com/api/1.4/xml/Autocomplete'

# this does not work in Rom2Rio Search API, lat,long work
# origin_place = 'Jama Masjid, New Delhi'
# dest_place = 'Ayyappa Swami Temple, Vijaya Bank Layout, Bangalore'

# origin_position = '28.646811,77.236252'  # Jama Masjid, New Delhi
# dest_position = '12.891430,77.606113'  # Ayyappa Swami Temple,Vijaya Bank Layout,Bangalore
# search_output = open(os.getcwd() + '\\files\\JamaMasjid_AyyappaswamyTemple', 'w')  # run it from onego_poc1 as current working dir

# def get_coordinates(place_string):      ## this is using Rom2Rio API, which does not work
#     auto_complete_args = {'key': api_token, 'query': place_string}
#     auto_complete_url = '{0}'.format(api_url_base_auto_complete)
#     response = requests.get(auto_complete_url, params=auto_complete_args)
#     print("Auto Complete API response: {}".format(str(response)))

gmaps = googlemaps.Client(key='Efr35fgrwwq')
def get_coordinates_google(place_string):
    geocode_res = gmaps.geocode(place_string)
    latitude = geocode_res[0]['geometry']['location']['lat']
    longitude = geocode_res[0]['geometry']['location']['lng']
    return latitude, longitude

origin_place = '3rd cross, 7th main, Vijaya Bank Layout, Bangalore'
dest_place = 'Rd Number 21 E, Rajeev Nagar, Patna'

lat, long = get_coordinates_google(origin_place)
origin_position = "{},{}".format(lat, long)
lat, long = get_coordinates_google(dest_place)
dest_position = "{},{}".format(lat, long)

# url_arguments_with_place_name = {'key': api_token, 'oName': origin_place, 'dName': dest_place}
url_arguments_with_place_latlong = {'key': api_token, 'oPos': origin_position, 'dPos': dest_position}


def get_route_info():
    api_url = '{0}'.format(api_url_base)
    response = requests.get(api_url, params= url_arguments_with_place_latlong)
    # print(response.url)
    # print(response.status_code) - success code - 200, failure code - others (400 - for wrong formatted url)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None

# To find coordintes using Auto Complete API, but does not work for 'Jama Masjid, New Delhi'
# get_coordinates(origin_place)
# get_coordinates(dest_place)


# To print Search API response to a file
route_info_json = get_route_info()
# search_output.write(str(route_info_json))
print(route_info_json['routes'])

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


print("Routes Data", '\n')
i = 0
for route_dict in route_info_json['routes']:
    i = i+1
    print("Route Number", i)
    for key, value in route_dict.items():
        if key != 'segments':
            print(key, "-----", value)
        else:
            print(key, '--------')
            for segment in value:
                print('\t\t', segment)
                print('\t\t', '-------')
    print("-----------------------------")
    print("-----------------------------")

