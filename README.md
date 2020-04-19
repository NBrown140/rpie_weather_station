# rpie_weather_station
RaspberryPie weather station


## Initial Setup

### Run setup script

`sudo sh setup.sh`

This will install InfluxDB, Grafana, Python3 and the required python packages. The script will also start the grafana and influx server sevices. To be sure the services are running:

`sudo systemctl status grafana-server`

`sudo systemctl status influxdb`

`sudo systemctl status telegraf`

### Setup I2C

`sudo sh setup_i2c.sh`

At the end of the script, `sudo raspi-config` will run and require user interaction.

Enter `5. Interfacing Options`, `A7 I2C`, `YES`. Then, `sudo reboot`.

Test it worked with:

`sudo i2cdetect -y 1`

### Run the app

`sudo sh start.sh`

This shell script will start grafana-server, influxdb and telegraf (if not already done), as well as execute the script `python3 weather_station.py` put it in the background and keep a log in your current directory.


### Customize Grafana

Grafana and InfluxDB run locally on the raspberry pie. This means you can access grafana from any device on your local network from a browser at:

`http://RPIE_IP:3000`

Custom grafana dashboards are available here:


## Sensors
### Temp sensor:  DS18B20
Uses one-wire interface
Need to setup one-wire interface on one of the gpio pins (default is usually gpio 4):

https://thepihut.com/blogs/raspberry-pi-tutorials/18095732-sensors-temperature-with-the-1-wire-interface-and-the-ds18b20

https://pinout.xyz/pinout/1_wire

### Humidity and Temp sensor: DHT11
Uses serial interface
Adafruit library already exists to interface sensor. Python library is adafruit-circuitpython-dht.

https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/python-setup

### Barometer: BMP180
Uses I2C interface.

https://tutorials-raspberrypi.com/raspberry-pi-and-i2c-air-pressure-sensor-bmp180/
https://github.com/adafruit/Adafruit_Python_BMP/blob/master/examples/simpletest.py


## Useful links:
- Telegraf: https://devconnected.com/how-to-setup-telegraf-influxdb-and-grafana-on-linux/

