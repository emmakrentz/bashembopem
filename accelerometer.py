import serial
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time
import datetime

current_time = datetime.datetime.now()

# serial setup
# replace with whatever port you're connected to (can check at the bottom right of your arduino ide window)
ser = serial.Serial('/dev/cu.usbmodem14301', 115200, timeout=1)

# initialize lists for storage
time_vals, x1_vals, y1_vals, z1_vals = [], [], [], []
x2_vals, y2_vals, z2_vals = [], [], []

# how long in s to collect data
# change for however long you want to collect for
duration = 60
start_time = time.time()

print("Reading data...")

while time.time() - start_time < duration:
    # input arduino motion values
    line = ser.readline().decode('utf-8').strip()
    print(line)
    
    try:
        values = list(map(int, line.split(' ')))
        if len(values) == 6:
            # store values
            x1, y1, z1, x2, y2, z2 = values
            elapsed_time = round(time.time() - start_time, 2)
            
            # store separate values
            time_vals.append(elapsed_time)
            x1_vals.append(x1)
            y1_vals.append(y1)
            z1_vals.append(z1)
            x2_vals.append(x2)
            y2_vals.append(y2)
            z2_vals.append(z2)

    except ValueError:
        print(f"Skipping invalid data: {line}")

ser.close()

# create dataset
data = pd.DataFrame({"time": time_vals, "x1": x1_vals, "y1": y1_vals, "z1": z1_vals, "x2": x2_vals, "y2": y2_vals, "z2": z2_vals})
data["accel1"] = data.apply(lambda row: [row["x1"], row["y1"], row["z1"]], axis=1)
data["accel2"] = data.apply(lambda row: [row["x2"], row["y2"], row["z2"]], axis=1)

data.to_csv(f'accelerometer_data_{current_time}')
