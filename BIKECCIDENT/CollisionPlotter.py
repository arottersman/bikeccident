import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from NYCGeoclientService import *
import BikeLaneParser
import AvenueNameConverter
import operator

BOROUGH = 'Manhattan'

def graph_bike_lane_pie_chart(collisions):
    onBikeLaneSum = 0
    offBikeLaneSum = 0
    unprocessable = 0
    bikeLaneDict = BikeLaneParser.getBikeLanes(BOROUGH)
    for collision in collisions:
        try:
            if(check_cross_streets_for_bike_lanes(collision, bikeLaneDict)):
                onBikeLaneSum = onBikeLaneSum + 1
            else:
                offBikeLaneSum = offBikeLaneSum + 1
        except ValueError:
            unprocessable = unprocessable + 1
    totalCollisions = float(onBikeLaneSum + offBikeLaneSum)
    if(totalCollisions == 0):
        print "No assessable bike lanes found."
        return

    print "Number of Collisions On Bike Lane: " + str(onBikeLaneSum)
    print "Number of Collisions Off Bike Lane: " + str(offBikeLaneSum)
    print "Number of Unprocessable Collisions: " + str(unprocessable)
    onBikeLanePercent = (onBikeLaneSum / totalCollisions)*100
    offBikeLanePercent = (offBikeLaneSum / totalCollisions)*100
    labels = 'On Bike Lane', 'Not On Bike Lane'
    sizes = [onBikeLanePercent, offBikeLanePercent]
    plt.rcParams['patch.linewidth'] = 0
    colors= ['#b2df8a', '#1f78b4']
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', shadow=False)
    # Set aspect ratio to be equal so that pie is drawn as a circle.
    plt.axis('equal')

    plt.show()

def check_cross_streets_for_bike_lanes(collision, bikeLaneDict):
    crossStreetOne = AvenueNameConverter.convert_avenue_name_from_numeral(
     collision.location.crossStreetOne)
    crossStreetTwo = AvenueNameConverter.convert_avenue_name_from_numeral(
     collision.location.crossStreetTwo)
    try:
        if(check_all_bike_lanes(crossStreetOne, collision.location, bikeLaneDict)):
            return True
        if(check_all_bike_lanes(crossStreetTwo, collision.location, bikeLaneDict)):
            return True
        return False
    except ValueError:
        raise ValueError

def check_all_bike_lanes(crossStreet, location, bikeLaneDict):
    if(crossStreet in bikeLaneDict):
        for bikeLane in bikeLaneDict[crossStreet]:
            try:
                if(bikeLane.isOnBikeLane(location)):
                    return True
            except ValueError:
                raise ValueError

def graph_contributing_factors(collisions):
    contributingFactors = dict()
    for collision in collisions:
        cf = "Not Reported" if collision.contributingFactor is '' else collision.contributingFactor
        if(cf in contributingFactors):
            contributingFactors[cf] += 1
        else:
            contributingFactors[cf] = 1
    key_value_tuple = create_sorted_keys_values_lists(contributingFactors)
    bar_chart(key_value_tuple[1], key_value_tuple[0],
        "Collisions", "Contributing Factors", "Contributing Factors")

def graph_hotspot_streets(collisions):
    streets = dict()
    for collision in collisions:
        if(collision.location.crossStreetOne in streets):
            streets[collision.location.crossStreetOne] += 1
        else:
            streets[collision.location.crossStreetOne] = 1
        if(collision.location.crossStreetTwo in streets):
            streets[collision.location.crossStreetTwo] += 1
        else:
            streets[collision.location.crossStreetTwo] = 1

    key_value_tuple = create_sorted_keys_values_lists(streets)
    bar_chart(key_value_tuple[1], key_value_tuple[0],
            "Collisions", "Streets", "Contributing Factors")


def graph_vehicle_type(collisions):
    vehicles = dict()
    for collision in collisions:
        addedBike = False
        for vehicle, vehicleSummary in collision.involvedVehicles:
            if(vehicleSummary in vehicles):
                if(vehicleSummary != "Bicycle"
                   or (vehicleSummary == "Bicycle" and addedBike == True)):
                    vehicles[vehicleSummary] += 1
            else:
                vehicles[vehicleSummary] = 1
                if(vehicleSummary == "Bicycle"):
                    addedBike = True
    key_value_tuple = create_sorted_keys_values_lists(vehicles)
    bar_chart(key_value_tuple[1], key_value_tuple[0],
        "Collisions", "Vehicles", "Contributing Factors")

def bar_chart(x_data, y_data, x_label, y_label, title):
    sns.set(style='white')

    axes = sns.barplot(x_data, y_data, palette="Set3")
    autolabel(axes.patches, axes)

    # Finalize the plot
    sns.axlabel(x_label,y_label)
    sns.despine(bottom=True)
    plt.setp(axes, xticks=[])
    plt.tight_layout(h_pad=3)

def autolabel(rects, ax):
    # attach some text labels to horizontal bar chart
    for rect in rects:
        width = rect.get_width()
        ax.text(width+1.10, rect.get_y()+rect.get_height()/2., '%s'%int(width))

def create_sorted_keys_values_lists(unsorted_dict, size_cutoff=15):
    keys = list()
    values = list()
    count = 0
    for key, value in reversed(sorted(unsorted_dict.iteritems(), key=operator.itemgetter(1))):
        keys.append(key)
        values.append(value)
        count +=1
        if(count>size_cutoff):
            break
    return [keys, values]
