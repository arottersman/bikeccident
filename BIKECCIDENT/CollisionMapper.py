import folium
import Collision, Location

orange = '#ff791a'
red = '#ff341a'
purple = '#2a0047'
blue = '#003e61'

def create_collision_map(collisions):
    map = folium.Map(location=[ 40.7902778, -73.9597222], zoom_start=12 ) #,tiles='Stamen Toner')
    print("Number of Collisions At Time of Mapping: ")
    print(len(collisions))
    for collision in collisions:
        if(collision.location.latitude != None):
            if(collision.numCyclistsKilled > 0):
                map.circle_marker([collision.location.latitude, collision.location.longitude],
                    radius=30,
                    popup=collision.contributingFactor,
                    line_color=purple,
                    fill_color=purple, fill_opacity=0.2)
            else:
                map.circle_marker([collision.location.latitude, collision.location.longitude],
                    radius=30,
                    popup=collision.contributingFactor,
                    line_color=blue,
                    fill_color=blue, fill_opacity=0.2)
    return map
