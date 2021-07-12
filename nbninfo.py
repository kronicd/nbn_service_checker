import requests
import time
import json
import urllib
from pprint import pprint

# Put your address here!
address = ""

locations = dict()
address = urllib.parse.quote_plus(address)


def getLocationIds():

    ts = int(time.time())
    url = f"https://places.nbnco.net.au:443/places/v1/autocomplete?query={address}&timestamp={ts}"

    payload = ""
    headers = {
        "Origin": "https://www.nbnco.com.au", 
        "Referer": "https://www.nbnco.com.au/", 
        "Connection": "close", 
        "Host": "places.nbnco.net.au", 
        "Accept-Encoding": "gzip, deflate", 
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
    }

    response = requests.request("GET", url, data=payload, headers=headers)
    jsonResp = json.loads(response.content)['suggestions']

    ids = set()

    for record in json.loads(response.content)['suggestions']:
        ids.add(record['id'])

    return ids

def getDetails(location_id):
    url = f"https://places.nbnco.net.au:443/places/v2/details/{location_id}"
    payload = ""
    headers = {
        "Origin": "https://www.nbnco.com.au", 
        "Referer": "https://www.nbnco.com.au/", 
        "Connection": "close", 
        "Host": "places.nbnco.net.au", 
        "Accept-Encoding": "gzip, deflate", 
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
    }

    response = requests.request("GET", url, data=payload, headers=headers)
    return json.loads(response.content)

while True:
    for _id in getLocationIds():
        details = getDetails(_id)
        details.pop("timestamp")
      
        if _id in locations.keys():
            if locations[_id] == details:
                pass
                #print(f"No new details for {_id}\n\n")
            else:
                print(f"New details for {_id}\n\n")
                locations[_id] = details
                pprint(locations[_id])
        else:
            print(f"New Location ID found: {_id}\n\n")
            locations[_id] = details
            pprint(locations[_id])
    time.sleep(10)
