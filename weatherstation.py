import os
import glob
import time
from datetime import datetime

from influxdb import InfluxDBClient

### Initialize db connection
# Connect to local db
client = InfluxDBClient(host='localhost', port=8086)
# Create db if not exist
client.create_database('weather_station')
# Print list of dbs
print(client.get_list_database())
# Connect to 'eather_station' db
client.switch_database('weather_station')


### Initialize sensors

## 1. Initialize Temp sensor
# GPIO pins
# Assumes /boot/config.txt already has line dtoverlay=w1-gpio
os.system('modprobe w1-gpio')  # Turns on the GPIO module
os.system('modprobe w1-therm') # Turns on the Temperature module

# Finds the correct device file that holds the temperature data
base_dir = "/sys/bus/w1/devices/"
device_folder = glob.glob(base_dir + "28*")[0]
device_file = device_folder + "/w1_slave"
print(f"base_dir: {base_dir}")
print(f"device_folder: {device_folder}")
print(f"device_file: {device_file}")


### Sensor read functions
def read_temp_raw(device_file):
    with open(device_file, 'r') as f:
        return f.readlines()


def read_temp(device_file, wait_interval=0.1):
    """Convert the value of the sensor into temp"""
    lines = read_temp_raw(device_file)
    # While the first line does not contain 'YES', wait for 0.2s
    # and then read the device file again
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(wait_interval)
        lines = read_temp_raw(device_file)

    # Look for position of the '=' in the second line
    equals_pos = lines[1].find('t=')

    # If the '=' is found,  convert the rest of the line into Celcius
    if equals_pos != -1:
        temp_str = lines[1][equals_pos+2:]
        temp_c = float(temp_str) / 1000.0
        return temp_c


### Run infinite loop
while True:
    # Get current datetime
    current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    # Read and store Temp sensor value
    temp = read_temp(device_file)
    print(temp, type(temp))
    json_body = [{
            "measurement": "tempSensor",
            "time": current_time,
            "fields": {
                "air_temp": temp}
            }]
    res_code = client.write_points(json_body)
    print(res_code)

    # Wait 1 second 
    time.sleep(1)



