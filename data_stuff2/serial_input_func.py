import serial
import time
import data_sim_mod as sim

ser = serial.Serial('COM3', 115200)
time.sleep(2)
print("Total locations defined:", len(sim.locations))

try:
    while True:
        for i, location in enumerate(sim.locations):
            data = sim.generate_data(location)
            ser.write((data + '\n').encode())
            print(f"[{i+1}] Sent: {data}")
            time.sleep(0.5)
        time.sleep(180)
except KeyboardInterrupt:
    print("Simulation stopped.")
    ser.close()