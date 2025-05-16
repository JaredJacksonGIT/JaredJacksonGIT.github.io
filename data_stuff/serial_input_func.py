import serial
import time
import data_sim_mod as sim

ser = serial.Serial('COM3', 115200)
time.sleep(2)

try:
    while True:
        data = sim.generate_data()
        ser.write((data + '\n').encode())
        print(f"Sent: {data}")
        time.sleep(5)
except KeyboardInterrupt:
    print("Simulation stopped.")
    ser.close()