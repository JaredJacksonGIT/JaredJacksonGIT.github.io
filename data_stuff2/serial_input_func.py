import serial
import time
import data_sim_mod as sim

pollutant_functions = {
    'PM25': sim.PM25,
    'PM10': sim.PM10,
    'NO2': sim.NO2,
    'CO': sim.CO,
    'CO2': sim.CO2,
    'VOC': sim.VOC,
    'CH4': sim.CH4,
    'O3': sim.O3
}

ser = serial.Serial('COM3', 115200)
time.sleep(2)

try:
    while True:
        for name, func in pollutant_functions.items():
            message_parts = [name]

            for location in sim.locations:
                value = func()[0]
                message_parts.append(f"{location[0]},{location[1]}:{value}") # Message currently in wrong format

            message = " ".join(message_parts)
            ser.write((message + '\n').encode())
            print(f"Sent: {message}")
            time.sleep(2)

        time.sleep(180)
except KeyboardInterrupt:
    print("Simulation stopped.")
    ser.close()