from collections import defaultdict
import json
import subprocess
import os
from data_stuff2.subscribe import message_queue, start_mqtt

script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, 'emissions_data')

# Container to hold the location and sensor readings SORTED BY POLLUTANT
pollution_data = defaultdict(lambda: defaultdict(list))

# Container to hold location and AQI SORTED BY POLLUTANT
pollutant_data = defaultdict(lambda: defaultdict(list))

EXPECTED_LOCATIONS = 110
received_locations = set()

# Breakpoints to calculate AQI (C_low, C_high, I_low, I_high)
# https://aqs.epa.gov/aqsweb/documents/codetables/aqi_breakpoints.html
breakpoints = {
    # PM2.5, PM10, N02, CO, CO2, VOCs, O3
    "PM25": [ # μg/m³
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

    "VOC": [ # ppm
        (0.0, 0.22, 0, 50),
        (0.221, 0.66, 51, 100),
        (0.661, 2.2, 101, 150),
        (2.201, 5.5, 151, 200),
    ],

    "CH4": [ # ppm
        (1.7, 50.0, 0, 50),
        (50.1, 150.0, 51, 100),
        (150.1, 300.0, 101, 150),
        (300.1, 500.0, 151, 200),
        (500.1, 750.0, 201, 300),
        (750.1, 1000.0, 301, 400)
    ],

    "O3": [ # ppm
        (20.0, 54.0, 0, 50),
        (54.1, 70.0, 51, 100),
        (70.1, 85, 101, 150),
        (85.1, 105.0, 151, 200),
        (105.1, 300.0, 201, 300)
    ]
}

def export_heat_data(filename, data):
    filepath = os.path.join(output_dir, filename)
    heatmap_data = [[lat, lon, sum(aqi)/len(aqi)] for (lat, lon), aqi in data.items() if len(aqi) > 0]
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

# Upload to git function
def upload_to_git(commit_msg):
    try:
        subprocess.run(["git", "pull"], check=True)
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push"], check=True)
    except subprocess.CalledProcessError as e:
        print("Error during Git upload: ", e)

start_mqtt()
print("Waiting for messages...")

while True:
    if not message_queue.empty():
        msg = message_queue.get()

        try:
            if isinstance(msg, list) and len(msg) == 1:
                line = msg[0].strip()
            else:
                line = msg.decode().strip() if isinstance(msg, bytes) else msg.strip()
                
            print("Received line:", line)
            parts = line.split()

            if len(parts) != 10:
                print("Invalid message format:", line)
                continue

            lat, lon = float(parts[0]), float(parts[1])
            values = list(map(float, parts[2:]))
            location = (lon, lat)

            if location in received_locations:
                print("Duplicate location received, skipping:", location)
                continue
            
            received_locations.add(location)

            for i, pollutant in enumerate(["PM25", "PM10", "NO2", "CO", "CO2", "VOC", "CH4", "O3"]):
                pollution_data[pollutant][location].append(values[i])
        
        except Exception as e:
            print("Error parsing message:", e)

        print(f"Currently received {len(received_locations)} of {EXPECTED_LOCATIONS} locations.")
        if len(received_locations) >= EXPECTED_LOCATIONS:
            print("All data received. Calculating AQI...")

            # Average out concentration values before calculating AQI
            for pollutant, locations in pollution_data.items(): # every location for each pollutant
                for location, values in locations.items(): # every value for each location
                    avg_concentration = sum(values) / len(values) # average it out
                    aqi = calculate_aqi(pollutant, round(avg_concentration)) # use pollutant and averaged concentration calculate AQI
                    if aqi is not None:
                        pollutant_data[pollutant][location].append((aqi)) # Assign the AQI of that pollutant to corresponding location

            # Generate separate JSON file for each pollutant
            for pol, locations in pollutant_data.items():
                filename = f"{pol.replace('.','').replace(' ','')}_data.json" # PM2.5 -> PM25_data.json
                export_heat_data(filename, locations)

            upload_to_git('Automated data upload')

            pollution_data.clear()
            pollutant_data.clear()
            received_locations.clear()
            print("Ready for next data cycle.\n")