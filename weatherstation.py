import os
import glob
import time
from datetime import datetime

from influxdb import InfluxDBClient
from  influxdb.exceptions import InfluxDBServerError
import board
import adafruit_dht

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

## 1. Initialize DS18B20 Temp sensor
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

## 2. Initialize DHT11 Humidity sensor on GPIO24
dhtDevice = adafruit_dht.DHT11(board.D24)


### Sensor read functions
def read_temp_raw(device_file):
    with open(device_file, 'r') as f:
        return f.readlines()


def read_temp_ds18b20(device_file, wait_interval=0.1):
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


def read_dht11():
    try:
        temperature_c = dhtDevice.temperature
        humidity = dhtDevice.humidity
        return humidity, temperature_c
    except Exception as e:
        print(e)
        return None, None


### Run infinite loop
while True:
    # Get current datetime
    current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    # Read and store temp ds18b20 sensor value
    ds18b20_temp = read_temp_ds18b20(device_file)
    # Read DHT11 humidity and temp
    dht11_hum, dht11_temp = read_dht11()
    print(current_time)
    print(ds18b20_temp)
    print(dht11_temp, dht11_hum)
    json_body = [{
            "measurement": "DS18B20",
            "time": current_time,
            "fields": {
                "temp": ds18b20_temp}
            }]
    if dht11_hum:
            json_body.append({
                "measurement": "DHT11",
                "time": current_time,
                "fields": {
                    "humidity": dht11_hum,
                    "temp": dht11_temp}
                })
    try:
        res_code = client.write_points(json_body)
        print(res_code)
    except InfluxDBServerError as e:
        print(e)
        continue

    # Wait 9 seconds 
    time.sleep(9)



