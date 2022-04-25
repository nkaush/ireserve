from calendar import c
from flask import render_template, make_response
from .utils import is_logged_in, get_user
from sqlalchemy import text
import folium
import pandas as pd

def create_map(db):
    # Make an empty map
    m = folium.Map(location=[20,0], tiles="OpenStreetMap", zoom_start=2)

    reservations = db.engine.execute("SELECT `BuildingName`, COUNT(`BuildingName`) AS res_count FROM `reservation` NATURAL JOIN `room` NATURAL JOIN `building` GROUP BY `BuildingName` ORDER BY `BuildingName`;")
    buildings = []
    counts = []

    for r in reservations:
        counts.append(r.res_count)
        buildings.append(r.BuildingName)
    
    print(counts)
    print(buildings)

    print(len(counts), len(buildings))
    
    data = pd.DataFrame({
   'lon':[-58, 2, 145, 30.32, -4.03, -73.57, 36.82, -38.5],
   'lat':[-34, 49, -38, 59.93, 5.33, 45.52, -1.29, -12.97],
   'name': buildings,
   'value': counts
    }, dtype=str)

    # add marker one by one on the map
    for i in range(0,len(data)):
        folium.Circle(
            location=[data.iloc[i]['lat'], data.iloc[i]['lon']],
            popup=data.iloc[i]['name'],
            radius=float(data.iloc[i]['value'])*20000,
            color='crimson',
            fill=True,
            fill_color='crimson'
        ).add_to(m)

    # Save map  
    m.save('templates/map.html')
