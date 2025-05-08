import serial
import time
import random

ser = serial.Serial('COM3', 115200)
time.sleep(2)

try:
    while True:
        co2 = round(random.uniform(400, 600), 1)
        ch4 = round(random.uniform(1.5, 2.5), 2)
        n2o = round(random.uniform(0.3, 0.5), 2)
        data = f"CO2:{co2},CH4:{ch4},N2O:{n2o}"
        ser.write((data + '\n').encode())
        print(f"Sent: {data}")
        time.sleep(5)
except KeyboardInterrupt:
    print("Simulation stopped.")
    ser.close()