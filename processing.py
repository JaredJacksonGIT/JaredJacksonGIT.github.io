from collections import defaultdict
import json

# TEMPORARY - replace with loop to process Jesara's simulated values
# take from the server and sort into this format (reading values from a json file?)
incoming_data = [
    {"location" : "location_a", "pollutant" : "PM2.5", "value" : 33.2},
    {"location" : "location_a", "pollutant" : "PM2.5", "value" : 30.8},
    {"location" : "location_a", "pollutant" : "PM10", "value" : 29.6},
    {"location" : "location_a", "pollutant" : "PM10", "value" : 30.2},

    {"location" : "location_b", "pollutant" : "CO2", "value" : 480.2},
    {"location" : "location_b", "pollutant" : "CO2", "value" : 473.5},
    {"location" : "location_b", "pollutant" : "N02", "value" : 53.2},
    {"location" : "location_b", "pollutant" : "N02", "value" : 49.8},

    {"location" : "location_c", "pollutant" : "PM2.5", "value" : 193.2},
    {"location" : "location_c", "pollutant" : "PM2.5", "value" : 203.1},
    {"location" : "location_c", "pollutant" : "VOCs", "value" : 0.572},
    {"location" : "location_c", "pollutant" : "VOCs", "value" : 0.551},
    {"location" : "location_c", "pollutant" : "VOCs", "value" : 0.492}
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

    "N02": [ # ppb
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

# AQI calculation formulas for each pollutant
def calculate_aqi(pol, conc):
    if pol not in breakpoints:
        return None # if the pollutant doesn't exist in breakpoints dictionary
    for C_low, C_high, I_low, I_high in breakpoints[pol]:
        if C_low <= conc <= C_high:
            return round(((I_high - I_low) / (C_high - C_low)) * (conc - C_low) + I_low)
    return None # if the conc doesn't afll within defined range

pollution_data = defaultdict(lambda: defaultdict(list))

# Organise concentration by location, then pollutant
for entry in incoming_data:
    location = entry["location"]
    pollutant = entry["pollutant"]
    concentration = entry["value"] # sensor reading (raw values)

    # put all concentrations into dictionary sorted by location and pollutant
    pollution_data[location][pollutant].append(concentration)
    #print(pollution_data) # ** so it's correctly taking all the values and sorting them. just not calculating aqi properly yet! **

# Average out concentration values before calculating AQI
for location in pollution_data: # every location
    for pollutant in pollution_data[location]: # every pollutant in each location
        all_concentrations = pollution_data[location][pollutant] # collect all concentrations for that pollutant in given location
        avg_concentration = round(sum(all_concentrations)) / (len(all_concentrations)) # average it out

        #print(pollution_data[location])
        #print(avg_concentration)

        aqi = calculate_aqi(pollutant, avg_concentration) # use pollutant and averaged concentration calculate AQI
        pollution_data[location][pollutant] = aqi # Assign the AQI of that pollutant to corresponding location

# Output pollution data
print(pollution_data)
with open('processing.json', 'w') as f: # write pollution data to json file
    json.dump(pollution_data, f, indent = 4) # format out into the json file