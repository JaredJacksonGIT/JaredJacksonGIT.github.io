from collections import defaultdict
import json
import subprocess
import os
from data_stuff2.subscribe import message_queue, start_mqtt
import time

script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, 'emissions_data')

# Container to hold the location and sensor readings SORTED BY POLLUTANT
pollution_data = defaultdict(lambda: defaultdict(list))

# Container to hold location and AQI SORTED BY POLLUTANT
pollutant_data = defaultdict(lambda: defaultdict(list))

EXPECTED_LOCATIONS = 107
MAX_WAIT_TIME = 120
received_locations = set()

# Breakpoints to calculate AQI (C_low, C_high, I_low, I_high)
# https://aqs.epa.gov/aqsweb/documents/codetables/aqi_breakpoints.html
breakpoints = {
    # PM2.5, PM10, N02, CO, CO2, VOC, O3
    "PM25": [ # μg/m³
        (0.0, 12.0, 0, 50),
        (12.1, 35.4, 51, 100),
        (35.5, 55.4, 101, 150),
        (55.5, 150.4, 151, 200),
        (150.5, 250.4, 201, 300)
    ],

    "PM10": [ # μg/m³
        (0.0, 54.0, 0, 50),
        (55.0, 154.0, 51, 100),
        (155.0, 254.0, 101, 150),
        (255.0, 354.0, 151, 200),
        (355.0, 424.0, 201, 300)
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
        (500.1, 750.0, 201, 300)
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
            return aqi/300.0
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
time.sleep(2)
print("Waiting for messages...")

while True:
    last_received_time = time.time()

    while len(received_locations) < EXPECTED_LOCATIONS:
        if not message_queue.empty():
            msg = message_queue.get()
            print("Received message dict:", msg)

            for entry in msg:
                location = (entry["long"], entry["lat"])
                pollutant = entry["pollutant"]
                value = float(entry["value"])

                pollution_data[pollutant][location].append(value)
                received_locations.add(location)

            print(f"Currently received {len(received_locations)} of {EXPECTED_LOCATIONS} locations.")
    
        if time.time() - last_received_time > MAX_WAIT_TIME:
            print("Timeout limit reached. Proceeding with available data.")
            break

        time.sleep(0.1)
        
    print("All data received. Calculating AQI...")

    for pollutant, locations in pollution_data.items():
        for location, values in locations.items():
            avg_concentration = sum(values) / len(values)
            aqi = calculate_aqi(pollutant, round(avg_concentration))
            if aqi is not None:
                pollutant_data[pollutant][location].append(aqi)

    for pol, locations in pollutant_data.items():
        filename = f"{pol.replace('.', '').replace(' ', '')}_data.json"
        export_heat_data(filename, locations)

    upload_to_git('Automated data upload')

    # Reset for next round
    pollution_data.clear()
    pollutant_data.clear()
    received_locations.clear()
    print("Ready for next data cycle.\n")