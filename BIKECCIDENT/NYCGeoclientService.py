# /https://api.cityofnewyork.us/geoclient/v1/intersection.json?crossStreetOne=broadway&crossStreetTwo=w 99 st&borough=manhattan&app_id=d02e0e27&app_key=bikeccident
import requests

import Properties
from Location import *

def getIntersectionCoordinates(borough, crossStreetOne, crossStreetTwo):
    url = Properties.GEOCLIENT_BASE_URL + "intersection.json"

    params = dict(
        crossStreetOne=crossStreetOne,
        crossStreetTwo=crossStreetTwo,
        borough=borough,
        app_id=Properties.GEOCLIENT_API_ID,
        app_key=Properties.GEOCLIENT_API_KEY
    )

    resp = requests.get(url=url, params=params)
    data = resp.json()
    try:
        intersection = data['intersection']
        return Location(crossStreetOne, crossStreetTwo,
            intersection['longitude'], intersection['latitude'])
    except KeyError:
        return Location(crossStreetOne, crossStreetTwo, None, None)
