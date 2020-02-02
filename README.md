# rpie_weather_station
RaspberryPie weather station


### InfluxDB

#### To install influxdb on debian stretch
`sudo sh install_influxdb.sh`

#### To run influxdb at startup (optional)
`sudo systemctl unmask influxdb`

`sudo systemctl enable influxdb`

#### To start influxdb
`sudo systemctl start influxdb`

or

`sudo service influxdb start`

### Temp sensor:  DS18B20
Uses one-wire interface
Need to setup one-wire interface on one of the gpio pins (default is usually gpio 4):

https://thepihut.com/blogs/raspberry-pi-tutorials/18095732-sensors-temperature-with-the-1-wire-interface-and-the-ds18b20

https://pinout.xyz/pinout/1_wire


