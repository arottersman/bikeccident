import pandas

import Properties
import CollisionDataParser

def fetchData():
    return fetchIntersectionData(Properties.MANHATTAN_INTERSECTIONS_URL)

def fetchIntersectionData(boroughURL):
    main_sheet = pandas.read_excel(io=boroughURL, sheetname = 0)
    contributing_factor_sheet = pandas.read_excel(io=boroughURL, sheetname = 1)
    return CollisionDataParser.parseIntersectionData(main_sheet, contributing_factor_sheet)
