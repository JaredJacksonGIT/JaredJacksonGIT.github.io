import random as rnd

def normalize(current, baseline, max_expected):
    intensity = (current - baseline) / (max_expected - baseline)
    return max(0.0, min(1.0, intensity))

def randPM25():
    baseline = 5
    max_expected = 100
    current = rnd.uniform(baseline, max_expected)  # µg/m³
    return normalize(current, baseline, max_expected)

def randPM10():
    baseline = 10
    max_expected = 150
    current = rnd.uniform(baseline, max_expected)  # µg/m³
    return normalize(current, baseline, max_expected)

def randNO2():
    baseline = 10
    max_expected = 150
    current = rnd.uniform(baseline, max_expected)  # ppb
    return normalize(current, baseline, max_expected)

def randCO():
    baseline = 0.1
    max_expected = 10
    current = rnd.uniform(baseline, max_expected)  # ppm
    return normalize(current, baseline, max_expected)

def randCO2():
    baseline = 400
    max_expected = 800
    current = rnd.uniform(baseline, max_expected)  # ppm
    return normalize(current, baseline, max_expected)

def randVOCs():
    baseline = 10
    max_expected = 500
    current = rnd.uniform(baseline, max_expected)  # µg/m³
    return normalize(current, baseline, max_expected)

def randO3():
    baseline = 30
    max_expected = 100
    current = rnd.uniform(baseline, max_expected)  # ppb
    return normalize(current, baseline, max_expected)
