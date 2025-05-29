import numpy as np
import random as rand
import serial
import time
import data_sim_mod as sim

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
    [-37.6937, 144.9173],  # Airport West
    [-37.6909, 144.9016],  # Gladstone Park
    
    [-37.6747, 144.9103],  # Broadmeadows
    [-37.6818, 144.9467],  # Campbellfield
    [-37.6717, 144.9435],  # Coolaroo
    [-37.6622, 144.9311],  # Dallas
    [-37.6489, 144.9053],  # Westmeadows
    [-37.6871, 145.0784],  # Bundoora
    [-37.6795, 145.0590],  # Mill Park
    [-37.6514, 145.0180],  # Epping
    [-37.6713, 145.0176],  # Lalor
    [-37.6793, 145.0097],  # Thomastown
    
    [-37.7155, 145.1425],  # Warrandyte
    [-37.8417, 145.1140],  # Mount Waverley
    [-37.8881, 145.0812],  # Chadstone
    [-37.9018, 145.0879],  # Oakleigh
    [-37.9100, 145.0897],  # Clayton
    [-37.9466, 145.1530],  # Springvale
    [-37.9653, 145.1692],  # Noble Park
    [-37.9886, 145.1923],  # Dandenong
    [-38.0164, 145.1577],  # Keysborough
    [-37.9352, 145.1857],  # Mulgrave
    
    [-37.9039, 145.1946],  # Wheelers Hill
    [-37.9042, 145.0064],  # Brighton
    [-37.9362, 145.0001],  # Sandringham
    [-37.9645, 145.0160],  # Black Rock
    [-37.9793, 145.0354],  # Beaumaris
    [-37.9671, 145.0526],  # Mentone
    [-37.9989, 145.0653],  # Mordialloc
    [-38.0117, 145.0794],  # Parkdale
    [-38.0213, 145.0966],  # Edithvale
    [-38.0291, 145.1034],  # Aspendale
    
    [-38.0345, 145.1106],  # Chelsea
    [-38.0673, 145.1260],  # Carrum
    [-38.1032, 145.1326],  # Seaford
    [-38.1461, 145.1223],  # Frankston
    [-37.8201, 144.9465],  # Docklands
    [-37.7926, 144.9385],  # Kensington
    [-37.7844, 144.9511],  # Parkville
    [-37.8023, 144.9783],  # Fitzroy
    [-37.8008, 144.9634],  # Carlton
    
    [-37.8120, 144.9839],  # East Melbourne
    [-37.8230, 144.9645],  # Southbank
    [-37.8255, 144.9541],  # South Wharf
    [-37.8425, 144.9612],  # Middle Park
    [-37.8448, 144.9739],  # Albert Park
    [-37.8522, 144.9930],  # Prahran
    [-37.8551, 144.9945],  # Windsor
    [-37.8858, 145.0030],  # Elsternwick
]


#normalise each value to between 0 - 1
def norm(min_expected, current, max_total):
    intensity = ((current - min_expected) / (max_total - min_expected))
    return intensity

def CO():
    min_expected = 0.1
    max_low = 10 #below this value returns low, above returns high
    max_total = 30

    current = rand.uniform(min_expected, max_total) #generated gas value
    intensity = norm(min_expected, current, max_total) #normalised value

    if ((current >= min_expected) and (current <= max_low)):
        strength = "LOW"
    elif current > max_low:
        strength = "HIGH"

    return [current, intensity, strength] #strength: high or low, in case we want to allow user to toggle gases 
                                          #and show severity of one gas at a time on the map

def CO2():
    min_expected = 400
    max_low = 1000 #ppm
    max_total = 5000

    current = rand.uniform(min_expected, max_total)
    intensity = norm(min_expected, current, max_total)

    if ((current >= min_expected) and (current <= max_low)):
        strength = "LOW"
    elif current > max_low:
        strength = "HIGH"

    return [current, intensity, strength]

def CH4():
    min_expected = 1.7
    max_low = 100; #ppm
    max_total = 1000

    current = rand.uniform(min_expected, max_total)
    intensity = norm(min_expected, current, max_total)

    if ((current >= min_expected) and (current <= max_low)):
        strength = "LOW"
    elif current > max_low:
        strength = "HIGH"

    return [current, intensity, strength]

def VOC():
    min_expected = 0.01
    max_low = 0.66 #ppm
    max_total = 2.2

    current = rand.uniform(min_expected, max_total)
    intensity = norm(min_expected, current, max_total)

    if ((current >= min_expected) and (current <= max_low)):
        strength = "LOW"
    elif current > max_low:
        strength = "HIGH"

    return [current, intensity, strength]

def PM25(): # pm2.5
    min_expected = 0.0
    max_low = 75 #μg/m3
    max_total = 300

    current = rand.uniform(min_expected, max_total)
    intensity = norm(min_expected, current, max_total)

    if ((current >= min_expected) and (current <= max_low)):
        strength = "LOW"
    elif current > max_low:
        strength = "HIGH"

    return [current, intensity, strength]

def PM10(): # pm10
    min_expected = 0.0
    max_low = 100 #μg/m3
    max_total = 300

    current = rand.uniform(min_expected, max_total)
    intensity = norm(min_expected, current, max_total)

    if ((current >= min_expected) and (current <= max_low)):
        strength = "LOW"
    elif current > max_low:
        strength = "HIGH"

    return [current, intensity, strength]

def NO2(): # nitrogen dioxide
    min_expected = 10
    max_low = 150 #ppb
    max_total = 360

    current = rand.uniform(min_expected, max_total)
    intensity = norm(min_expected, current, max_total)

    if ((current >= min_expected) and (current <= max_low)):
        strength = "LOW"
    elif current > max_low:
        strength = "HIGH"

    return [current, intensity, strength]

def O3(): # ozone
    min_expected = 20
    max_low = 125 #ppb
    max_total = 300

    current = rand.uniform(min_expected, max_total)
    intensity = norm(min_expected, current, max_total)

    if ((current >= min_expected) and (current <= max_low)):
        strength = "LOW"
    elif current > max_low:
        strength = "HIGH"

    return [current, intensity, strength]


def generate_data(location):
    loc_PM25 = PM25()
    loc_PM10 = PM10()
    loc_NO2 = NO2()
    loc_CO = CO()
    loc_CO2 = CO2()
    loc_VOC = VOC()
    loc_CH4 = CH4()
    loc_O3 = O3()

    return f"{location[0]} {location[1]} {loc_PM25[0]} {loc_PM10[0]} {loc_NO2[0]} {loc_CO[0]} {loc_CO2[0]} {loc_CH4[0]} {loc_VOC[0]} {loc_O3[0]}"