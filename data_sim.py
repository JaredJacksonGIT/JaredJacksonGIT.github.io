import numpy as np
import random as rand

#dummy locations for now from heatmap test, will change once we decide on proper locations
locations = [
    [-37.822740, 145.037103],
    [-37.82258939, 145.03716513],
    [-37.82243878, 145.03722727],
    [-37.82228817, 145.0372894],
    [-37.82213756, 145.03735153],
    [-37.82198695, 145.03741367],
    [-37.82183634, 145.0374758],
    [-37.82168573, 145.03753793],
    [-37.82153512, 145.03760007],
    [-37.82138451, 145.0376622],

    [-37.82280667, 145.03728158],
    [-37.8226549, 145.03734525],
    [-37.82250313, 145.03740893],
    [-37.82235136, 145.0374726],
    [-37.82219959, 145.03753628],
    [-37.82204782, 145.03759995],
    [-37.82189605, 145.03766363],
    [-37.82174428, 145.0377273],
    [-37.82159251, 145.03779098],
    [-37.82144074, 145.03785465],

    [-37.82287333, 145.03746016],
    [-37.82272042, 145.03752536],
    [-37.8225675, 145.03759056],
    [-37.82241459, 145.03765576],
    [-37.82226168, 145.03772097],
    [-37.82210876, 145.03778617],
    [-37.82195585, 145.03785137],
    [-37.82180294, 145.03791657],
    [-37.82165002, 145.03798178],
    [-37.82149711, 145.03804698],

    [-37.82294, 145.03763873],
    [-37.82278594, 145.03770547],
    [-37.82263189, 145.03777222],
    [-37.82247783, 145.03783896],
    [-37.82232377, 145.0379057],
    [-37.82216971, 145.03797245],
    [-37.82201566, 145.03803919],
    [-37.8218616, 145.03810593],
    [-37.82170754, 145.03817268],
    [-37.82155348, 145.03823942],

    [-37.82300667, 145.0378173],
    [-37.82285147, 145.03788558],
    [-37.82269627, 145.03795387],
    [-37.82254106, 145.03802215],
    [-37.82238586, 145.03809043],
    [-37.82223066, 145.03815872],
    [-37.82207545, 145.038227],
    [-37.82192025, 145.03829528],
    [-37.82176505, 145.03836357],
    [-37.82160984, 145.03843185],

    [-37.82307333, 145.03799588],
    [-37.822917, 145.0380657],
    [-37.82276067, 145.03813552],
    [-37.82260433, 145.03820533],
    [-37.822448, 145.03827515],
    [-37.82229167, 145.03834497],
    [-37.82213533, 145.03841478],
    [-37.821979, 145.0384846],
    [-37.82182267, 145.03855442],

    [-37.82166633, 145.03862423],
    [-37.82314, 145.03817445],
    [-37.82298253, 145.0382458],
    [-37.82282506, 145.03831714],
    [-37.8226676, 145.03838849],
    [-37.82251013, 145.03845983],
    [-37.82235266, 145.03853118],
    [-37.8221952, 145.03860252],
    [-37.82203773, 145.03867387],
    [-37.82188026, 145.03874521],

    [-37.8217228, 145.03881656],
    [-37.82320667, 145.03835303],
    [-37.82304807, 145.03842592],
    [-37.82288947, 145.03849882],
    [-37.82273087, 145.03857172],
    [-37.82257227, 145.03864462],
    [-37.82241367, 145.03871751],
    [-37.82225507, 145.03879041],
    [-37.82209647, 145.03886331],
    [-37.82193787, 145.0389362],

    [-37.82177927, 145.0390091],
    [-37.82327333, 145.0385316],
    [-37.8231136, 145.03860603],
    [-37.82295387, 145.03868047],
    [-37.82279413, 145.0387549],
    [-37.8226344, 145.03882933],
    [-37.82247467, 145.03890376],
    [-37.82231493, 145.0389782],
    [-37.8221552, 145.03905263],
    [-37.82199547, 145.03912706],

    [-37.82183573, 145.0392015],
    [-37.82334, 145.03871018],
    [-37.82317913, 145.03878614],
    [-37.82301827, 145.03886211],
    [-37.8228574, 145.03893808],
    [-37.82269653, 145.03901404],
    [-37.82253567, 145.03909001],
    [-37.8223748, 145.03916597],
    [-37.82221393, 145.03924194],
    [-37.82205307, 145.03931791],

    [-37.8218922, 145.03939387],
    [-37.82340667, 145.03888875],
    [-37.82324467, 145.03896624],
    [-37.82308267, 145.03904374],
    [-37.82292067, 145.03912123],
    [-37.82275867, 145.03919873],
    [-37.82259667, 145.03927622],
    [-37.82243467, 145.03935372],
    [-37.82227267, 145.03943121],
    [-37.82211067, 145.03950871],
    [-37.82194867, 145.0395862],
]

#normalise each value to between 0 - 1
def norm(min_expected, current, max_total):
    intensity = ((current - min_expected) / (max_total - min_expected))
    return intensity

def CO():
    min_expected = 0.1;
    max_low = 10; #below this value returns low, above returns high
    max_total = 30;

    current = rand.uniform(min_expected, max_total) #generated gas value
    intensity = norm(min_expected, current, max_total) #normalised value

    if ((current >= min_expected) and (current <= max_low)):
        strength = "LOW"
    elif current > max_low:
        strength = "HIGH"

    return [current, intensity, strength] #strength: high or low, in case we want to allow user to toggle gases 
                                          #and show severity of one gas at a time on the map

def CO2():
    min_expected = 400;
    max_low = 1000; #ppm
    max_total = 5000;

    current = rand.uniform(min_expected, max_total)
    intensity = norm(min_expected, current, max_total)

    if ((current >= min_expected) and (current <= max_low)):
        strength = "LOW"
    elif current > max_low:
        strength = "HIGH"

    return [current, intensity, strength]

def CH4():
    min_expected = 1.7;
    max_low = 100; #ppm
    max_total = 1000;

    current = rand.uniform(min_expected, max_total)
    intensity = norm(min_expected, current, max_total)

    if ((current >= min_expected) and (current <= max_low)):
        strength = "LOW"
    elif current > max_low:
        strength = "HIGH"

    return [current, intensity, strength]

def VOC():
    min_expected = 0.01;
    max_low = 0.66 #ppm
    max_total = 2.2;

    current = rand.uniform(min_expected, max_total)
    intensity = norm(min_expected, current, max_total)

    if ((current >= min_expected) and (current <= max_low)):
        strength = "LOW"
    elif current > max_low:
        strength = "HIGH"

    return [current, intensity, strength]

#just printing normalised average for each location for now, change to import into server
#just 1 generation for now, will add a timed while loop or something to continually update heatmap with new values
n = 1;
for location in locations:
    loc_CO = CO()
    loc_CO2 = CO2()
    loc_CH4 = CH4()
    loc_VOC = VOC()

    avg_intensity = ((loc_CO[1] + loc_CO2[1] + loc_CH4[1]) + loc_VOC[1]/ 4) #average of normalised values
    print(f"{n}: {avg_intensity:.2f}")
    n = n + 1;
