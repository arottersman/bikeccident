import Properties
import requests

def getDistance(origin, destination):
    data = getDirections(origin, destination)
    try:
        routes = data['routes']
        legs = routes[0]['legs']
        distance = legs[len(legs)-1]['distance']['value']
        return distance
    except(KeyError, IndexError):
        return -1

def getDirections(origin, destination):
    url = Properties.GOOGLE_DIRECTIONS_BASE_URL + "json"

    params = dict(
        origin=str(origin.latitude)+','+str(origin.longitude),
        destination=str(destination.latitude)+','+str(destination.longitude),
        mode='walking',
        key=Properties.GOOGLE_DIRECTIONS_API_KEY
    )
    resp = requests.get(url=url, params=params)
    return resp.json()
