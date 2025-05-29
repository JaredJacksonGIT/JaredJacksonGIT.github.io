import serial
import time
import data_sim_mod as sim

ser = serial.Serial('COM3', 115200)
time.sleep(2)

try:
    while True:
        for location in sim.locations:
            data = sim.generate_data(location)
            ser.write((data + '\n').encode())
            print(f"Sent: {data}")
            time.sleep(2)
        time.sleep(180)
except KeyboardInterrupt:
    print("Simulation stopped.")
    ser.close()