from collections import defaultdict
import json
import subprocess
import os

script_dir  = os.path.dirname(os.path.abspath(__file__))
output_dir  = os.path.join(script_dir, 'emissions_data')

# TEMPORARY - replace with loop to process Jesara's simulated values off the server
incoming_data = [
    # PM2.5 readings at Melbourne CBD and Carlton
    {"long": -37.8136, "lat": 144.9631, "pollutant": "PM2.5", "value": 33.2},
    {"long": -37.8000, "lat": 144.9636, "pollutant": "PM2.5", "value": 30.8},

    # PM10 readings at Fitzroy and Southbank
    {"long": -37.7982, "lat": 144.9790, "pollutant": "PM10",  "value": 29.6},
    {"long": -37.8203, "lat": 144.9640, "pollutant": "PM10",  "value": 30.2},

    # CO2 readings at St Kilda and Richmond
    {"long": -37.8675, "lat": 144.9785, "pollutant": "CO2",   "value": 480.2},
    {"long": -37.8236, "lat": 144.9832, "pollutant": "CO2",   "value": 473.5},

    # NO2 readings at Brunswick and Collingwood
    {"long": -37.7750, "lat": 144.9660, "pollutant": "NO2",   "value": 53.2},
    {"long": -37.8002, "lat": 144.9793, "pollutant": "NO2",   "value": 49.8},

    # VOC readings at Docklands and Port Melbourne
    {"long": -37.8167, "lat": 144.9460, "pollutant": "VOCs",  "value": 0.572},
    {"long": -37.8366, "lat": 144.9102, "pollutant": "VOCs",  "value": 0.551},
    {"long": -37.8167, "lat": 144.9460, "pollutant": "VOCs",  "value": 0.492},
]

# Breakpoints to calculate AQI (C_low, C_high, I_low, I_high)
# https://aqs.epa.gov/aqsweb/documents/codetables/aqi_breakpoints.html
breakpoints = {
    # PM2.5, PM10, N02, CO, CO2, VOCs, O3
    "PM2.5": [ # μg/m³
        (0.0, 12.0, 0, 50),
        (12.1, 35.4, 51, 100),
        (35.5, 55.4, 101, 150),
        (55.5, 150.4, 151, 200),
        (150.5, 250.4, 201, 300),
        (250.5, 350.4, 301, 400),
        (350.5, 500.4, 401, 500)
    ],

    "PM10": [ # μg/m³
        (0.0, 54.0, 0, 50),
        (55.0, 154.0, 51, 100),
        (155.0, 254.0, 101, 150),
        (255.0, 354.0, 151, 200),
        (355.0, 424.0, 201, 300),
        (425.0, 504.0, 301, 400),
        (505.0, 604.0, 401, 500)
    ],

    "NO2": [ # ppb
        (0.0, 53.0, 0, 50),
        (54.0, 100.0, 51, 100),
        (101.0, 360.0, 101, 150),
        (361.0, 649.0, 151, 200)
    ],

    "CO": [ # ppm
        (0.0, 53.0, 0, 50),
        (54.0, 100.0, 51, 100),
        (101.0, 360.0, 101, 150),
        (361.0, 649.0, 151, 200)
    ],

    "CO2": [ # ppm
        (400, 1000, 0, 50),
        (1001, 2000, 51, 100),
        (2001, 5000, 101, 150),
        (5001, 10000, 151, 200),
        (10001, 40000, 201, 300)
    ],

    "VOCs": [ # ppm
        (0.0, 0.220, 0, 50),
        (0.221, 0.660, 51, 100),
        (0.661, 2.200, 101, 150),
        (2.201, 5.500, 151, 200),
        (5.501, 11.000, 201, 300),
        (11.001, 22.000, 301, 400)
    ],

    "O3": [ # ppm
        (0.0, 0.054, 0, 50),
        (0.055, 0.070, 51, 100),
        (0.071, 0.085, 101, 150),
        (0.086, 0.105, 151, 200),
        (0.106, 0.200, 201, 300)
    ]
}

def export_heat_data(filename, data):
    filepath = os.path.join(output_dir, filename)
    heatmap_data = [[lat, lon, aqi[0]] for (lat, lon), aqi in data.items()]
    with open(filepath, 'w') as f:
        json.dump(heatmap_data, f)

# AQI calculation formulas for each pollutant
def calculate_aqi(pol, conc):
    if pol not in breakpoints:
        return None # if the pollutant doesn't exist in breakpoints dictionary
    for C_low, C_high, I_low, I_high in breakpoints[pol]:
        if C_low <= conc <= C_high:
            aqi = round( ((I_high - I_low) / (C_high - C_low)) * (conc - C_low) + I_low)
            return aqi/500.0
    return None # if the conc doesn't afll within defined range

# Container to hold the location and sensor readings SORTED BY POLLUTANT
pollution_data = defaultdict(lambda: defaultdict(list))

# Pair readings with the location SORTED BY POLLUTANT (long, lat, value)
for entry in incoming_data:
    location = (entry["long"], entry["lat"])
    pollutant = entry["pollutant"]
    value = entry["value"] # sensor reading (raw values)

    pollution_data[pollutant][location].append(value)
    #print(pollution_data)

# Container to hold location and AQI SORTED BY POLLUTANT
pollutant_data = defaultdict(lambda: defaultdict(list))

# Average out concentration values before calculating AQI
for pollutant, locations in pollution_data.items(): # every location for each pollutant
    for location, values in locations.items(): # every value for each location
        avg_concentration = sum(values) / len(values) # average it out

        aqi = calculate_aqi(pollutant, round(avg_concentration)) # use pollutant and averaged concentration calculate AQI
        pollutant_data[pollutant][location].append((aqi)) # Assign the AQI of that pollutant to corresponding location
        #print(pollutant_data)

# Generate separate JSON file for each pollutant
for pol, locations in pollutant_data.items():
    filename = f"{pol.replace('.','').replace(' ','')}_data.json" # PM2.5 -> PM25_data.json
    export_heat_data(filename, locations)

# Upload to git function
def upload_to_git(commit_msg):
    try:
        subprocess.run(["git", "pull"], check=True)
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push"], check=True)
    except subprocess.CalledProcessError as e:
        print("Error during Git upload: ", e)

upload_to_git('test message please work i pray')