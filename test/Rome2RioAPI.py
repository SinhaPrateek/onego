import json
import requests

# For more info on API - https://www.rome2rio.com/documentation/1-4/search/
# regrading using request library for querying through a url -https://2.python-requests.org//en/latest/user/quickstart/

api_token = 'bfOhgi4x'
api_url_base = 'http://free.rome2rio.com/api/1.4/json/Search'

origin_palce = 'delhi'
dest_place = 'patna'

url_arguments = {'key':api_token,'oName':origin_palce,'dName':dest_place}

def get_route_info():

    api_url = '{0}'.format(api_url_base)

    response = requests.get(api_url, params=url_arguments)
    #print(response.url)
    #print(response.status_code) - success code - 200, failure code - others (400 - for wrong formatted url)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None

route_info_json = get_route_info()
print(route_info_json['routes'])
