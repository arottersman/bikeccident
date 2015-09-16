import pandas
import IntersectionDataColumnName
from Location import *
from Collision import *
from NYCGeoclientService import *

def parseIntersectionData(main_sheet, contributing_factor_sheet):
    collisions = parseCollisions(main_sheet, "manhattan")
    collisions = parseContributingFactors(contributing_factor_sheet, collisions)
    return collisions

def parseCollisions(main_sheet, borough):
    data = main_sheet.loc[main_sheet[IntersectionDataColumnName.BICYCLE]>0]
    collisions = []
    iterrows = data.iterrows()
    next(iterrows)
    for index, row in iterrows:
        intersection_string = row[IntersectionDataColumnName.LOCATION]
        location = createLocationfromIntersectionString(borough, intersection_string)
        collisions.append( Collision(location,
                                    row[IntersectionDataColumnName.NUM_CYCLISTS_KILLED],
                                    row[IntersectionDataColumnName.NUM_CYCLISTS_INJURED],
                                    row[IntersectionDataColumnName.COLLISION_ID],
                                    row[IntersectionDataColumnName.COLLISION_KEY]))
    return collisions

def parseContributingFactors(contributingFactorSheet, collisions):
    for collision in collisions:
        data = contributingFactorSheet.loc[contributingFactorSheet[
            IntersectionDataColumnName.CONTRIB_COLLISION_ID] == collision.collisionId]
        for index, row in data.iterrows():
            if(not(pandas.isnull(row[IntersectionDataColumnName.CONTRIBUTING_FACTOR]))):
                collision.contributingFactor = row[IntersectionDataColumnName.CONTRIBUTING_FACTOR]
            collision.add_involved_vehicle([row[IntersectionDataColumnName.VEHICLE_TYPE_CODE],
                                            row[IntersectionDataColumnName.VEHICLE_TYPE_DESCRIPTION]])
    return collisions
    
def createLocationfromIntersectionString(borough, intersection_string):
    intersection_strings = intersection_string.split("&&")
    return getIntersectionCoordinates(borough, intersection_strings[0].strip(), intersection_strings[1].strip())
