# rpie_weather_station
RaspberryPie weather station


## Initial Setup

### Run setup script

`sudo sh setup.sh`

This will install InfluxDB, Grafana, Python3 and the required python packages. The script will also start the grafana and influx server sevices. To be sure the services are running:

`sudo systemctl status grafana-server`

`sudo systemctl status influxdb`

## Run the app
`python3 weather_station.py`


## Temp sensor:  DS18B20
Uses one-wire interface
Need to setup one-wire interface on one of the gpio pins (default is usually gpio 4):

https://thepihut.com/blogs/raspberry-pi-tutorials/18095732-sensors-temperature-with-the-1-wire-interface-and-the-ds18b20

https://pinout.xyz/pinout/1_wire


