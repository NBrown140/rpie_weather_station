import os
import glob
import time

# Initialize GPIO pins
# Assumes /boot/config.txt alreaady has line dtoverlay=w1-gpio
os.system('modprobe w1-gpio')  # Turns on the GPIO module
os.system('modprobe w1-therm') # Turns on the Temperature module

# Finds the coorectr device file rtaht holds the temperature data
base_dir = "/sys/bus/w1/devices/"
device_folder = glob.glob(base_dir + "28*")[0]
device_file = device_folder + "/w1_slave"
print(f"base_dir: {base_dir}")
print(f"device_folder: {device_folder}")
print(f"device_file: {device_file}")


def read_temp_raw(device_file):
    with open(device_file, 'r') as f:
        return f.readlines()

# Convert the value of the sensot into temp
def read_temp(device_file):
    lines = read_temp_raw(device_file)
    # While the first line does not contain 'YES', wait for 0.2s
    # and then read the device file again
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw(device_file)
        
    # Look for the position of the '=' in the sceond line
    equals_pos = lines[1].find('t=')

    # If the '=' is found,  convert the rest of the line into Celcius
    if equals_pos != -1:
        temp_str = lines[1][equals_pos+2:]
        temp_c = float(temp_str) / 1000.0

        return temp_c

if __name__ == "__main__":
    while True:
        print(read_temp_raw(device_file))
        
        print(read_temp(device_file))

        time.sleep(1)
