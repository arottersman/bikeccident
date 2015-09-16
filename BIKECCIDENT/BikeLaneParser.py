## This module contains the BikeLane object and the parser that
## reads from the data folder's lane-list.shtml. Use it to get
## all bike lanes in manhattan. Each bike lane object can test if a Location
## is contained on it
import GoogleDirectionsServiceBroker
from NYCGeoclientService import *
import Location
import lxml
import lxml.html
from os import path
import re

class BikeLane(object):
    def __init__(self, laneType, start, end, street):
        self.laneType = laneType
        self.start = start
        self.end = end
        self.street = street
        self.distance = GoogleDirectionsServiceBroker.getDistance(self.start, self.end)

    def isOnBikeLane(self, location, sensitivity=10):
        start_to_point = GoogleDirectionsServiceBroker.getDistance(self.start, location)
        point_to_end = GoogleDirectionsServiceBroker.getDistance(location, self.end)
        distance_sum = start_to_point + point_to_end
        if(start_to_point == -1 | point_to_end == -1 | self.distance == -1):
            raise ValueError
        if(distance_sum < (self.distance + sensitivity) and
            distance_sum > (self.distance - sensitivity)):
                return True
        return False

def getBikeLanes(borough):
    file_path = path.relpath("data/lane-list.shtml")
    with open(file_path) as bikeLaneHTML:
        html = lxml.html.fromstring(bikeLaneHTML.read())
        return parseBikeLaneList(borough,html)

def parseBikeLaneList(borough, html):
    ##returns a dict with streets as keys, and list of bike lanes
    ##as values.
    xpath_to_table = "body/div/section/div/table/tbody/tr"
    rows = html.xpath(xpath_to_table)
    bikeLaneDict = dict()
    for row in rows:
        if(row.getchildren()[2].text == borough):
            location_tuple = parseBikeLaneLocationString(row.getchildren()[0].text)
            street = location_tuple[0]
            start_street = location_tuple[1]
            end_street = location_tuple[2]
            start = getIntersectionCoordinates(borough, street, start_street)
            end = getIntersectionCoordinates(borough, street, end_street)
            if(start.latitude != None and end.latitude != None):
                if(street in bikeLaneDict):
                    bikeLanes = bikeLaneDict[street]
                else:
                    bikeLanes = list()
                bikeLanes.append(BikeLane(row.getchildren()[1].text, start, end, street))
                bikeLaneDict[street] = bikeLanes
    return bikeLaneDict

def parseBikeLaneLocationString(location):
    location_caps = location.upper()
    split_string = re.split(r'(\b FROM \b|\b TO \b|\b AND \b)', location_caps)
    return [split_string[0], split_string[2], split_string[4]]
