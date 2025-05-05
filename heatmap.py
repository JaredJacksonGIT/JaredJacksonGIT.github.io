from numbergenerator import * 
import json 

lat_min, lat_max = -38.1, -37.5
lon_min, lon_max = 144.5, 145.5
lat_step = 0.009
lon_step = 0.012

locations = []
lat = lat_min
while lat < lat_max:
    lon = lon_min
    while lon < lon_max:
        locations.append([round(lat, 6), round(lon, 6)])
        lon += lon_step
    lat += lat_step


PM25array = [randPM25() for _ in range(len(locations))]
PM10array = [randPM10() for _ in range(len(locations))]
NO2array  = [randNO2() for _ in range(len(locations))]
COarray   = [randCO() for _ in range(len(locations))]
CO2array  = [randCO2() for _ in range(len(locations))]
VOCsarray = [randVOCs() for _ in range(len(locations))]
O3array   = [randO3() for _ in range(len(locations))]

def export_heat_data(filename, array):
    heat_data = [[lat, lon, intensity] for (lat, lon), intensity in zip(locations, array)]
    with open(filename, "w") as f:
        json.dump(heat_data, f)

export_heat_data("PM25_data.json", PM25array)
export_heat_data("CO_data.json", COarray)
export_heat_data("PM10_data.json", PM10array)
export_heat_data("CO2_data.json", CO2array)
export_heat_data("NO2_data.json", NO2array)
export_heat_data("O3_data.json", O3array)
export_heat_data("VOCs_data.json", VOCsarray)