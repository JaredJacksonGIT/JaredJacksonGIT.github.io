from numbergenerator import * 
import json 

# Generate intensities for 3 locations
PM25array = []
PM10array = []
NO2array = []
COarray = []
CO2array = []
VOCsarray = []
O3array = []

for _ in range(100):
    intensity = randPM25()
    PM25array.append(intensity)

for _ in range(100):
    intensity = randPM10()
    PM10array.append(intensity)
    
for _ in range(100):
    intensity = randNO2()
    NO2array.append(intensity)

for _ in range(100):
    intensity = randCO()
    COarray.append(intensity)

for _ in range(100):
    intensity = randCO2()
    CO2array.append(intensity)

for _ in range(100):
    intensity = randVOCs()
    VOCsarray.append(intensity)

for _ in range(100):
    intensity = randO3()
    O3array.append(intensity)

locations = [
    [-37.8136, 144.9631],  # Melbourne
    [-37.8399, 144.9390],  # Port Melbourne
    [-37.8390, 144.9958],  # South Yarra
    [-37.8183, 145.0018],  # Richmond
    [-37.8270, 145.0352],  # Hawthorn
    [-37.8065, 145.0306],  # Kew
    [-37.7700, 144.9614],  # Brunswick
    [-37.7650, 144.9209],  # Moonee Ponds
    [-37.7480, 144.9115],  # Essendon
    [-37.7992, 144.8996],  # Footscray
    [-37.7749, 144.8925],  # Maribyrnong
    [-37.7885, 144.8322],  # Sunshine
    [-37.8062, 144.8188],  # Sunshine West
    [-37.7982, 144.8566],  # Braybrook
    [-37.7492, 144.8008],  # St Albans
    [-37.7286, 144.8001],  # Kings Park
    [-37.7671, 144.7867],  # Deer Park
    [-37.7771, 144.7520],  # Ravenhall
    [-37.8090, 144.7981],  # Derrimut
    [-37.8106, 144.7473],  # Truganina
    [-37.8672, 144.8307],  # Altona
    [-37.8734, 144.7722],  # Altona Meadows
    [-37.8682, 144.7503],  # Williams Landing
    [-37.8634, 144.7707],  # Laverton
    [-37.8423, 144.8875],  # Newport
    [-37.8129, 144.8930],  # Yarraville
    [-37.8676, 144.8994],  # Williamstown
    [-37.8676, 144.9805],  # St Kilda
    [-37.8814, 144.9845],  # Elwood
    [-37.7046, 144.9353],  # Glenroy
    [-37.7007, 144.9633],  # Fawkner
    [-37.7430, 144.9631],  # Coburg
    [-37.7382, 145.0018],  # Preston
    [-37.7161, 145.0064],  # Reservoir
    [-37.7024, 145.1039],  # Greensborough
    [-37.7051, 145.0719],  # Watsonia
    [-37.7173, 145.0715],  # Macleod
    [-37.7326, 145.0601],  # Rosanna
    [-37.7389, 145.0791],  # Viewbank
    [-37.7223, 145.1499],  # Eltham
    [-37.7568, 145.1171],  # Templestowe
    [-37.7563, 145.0715],  # Bulleen
    [-37.7800, 145.0726],  # Balwyn North
    [-37.8124, 145.0790],  # Balwyn
    [-37.8183, 145.1256],  # Box Hill
    [-37.8252, 145.1019],  # Surrey Hills
    [-37.8357, 145.1066],  # Wattle Park
    [-37.8497, 145.1113],  # Burwood
    [-37.8576, 145.1337],  # Burwood East
    [-37.8627, 145.1911],  # Vermont
    [-37.8731, 145.1928],  # Vermont South
    [-37.8770, 145.1663],  # Glen Waverley
    [-37.7455, 144.8671],  # Keilor East
    [-37.7276, 144.8320],  # Keilor
    [-37.6914, 144.8833],  # Tullamarine
    [-37.6989, 144.7823],  # Sydenham
    [-37.7076, 144.7476],  # Taylors Hill
    [-37.7423, 144.7437],  # Caroline Springs
]

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