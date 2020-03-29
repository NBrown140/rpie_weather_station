# Use to install and start influxdb on raspbian stretch

# The usual update and upgrade
apt -y update
apt -y upgrade


# Install required helper programs
apt-get -y install wget

### Install InfluxDB ###
# Get repository key
wget -qO- https://repos.influxdata.com/influxdb.key | sudo apt-key add -
# Add repository to the sources list
echo "deb https://repos.influxdata.com/debian buster stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
# Update again
apt -y update
# Install
apt -y install influxdb


### Install grafana ###
apt-get install -y adduser libfontconfig1
wget https://dl.grafana.com/oss/release/grafana-rpi_6.7.1_armhf.deb
dpkg -i grafana-rpi_6.7.1_armhf.deb


### Start InfluxDB service ###
systemctl start influxdb  # OR service influxdb start
# Start at boot
systemctl unmask influxdb
systemctl enable influxdb 


### Start Grafana service ###
systemctl daemon-reload
systemctl start grafana-server
# Start at boot
systemctl enable grafana-server.service


### Install python3 and packages ###
apt -y install python3 python3-pip
python3 -m pip install -U pip setuptools
python3 -m pip install -r requirements.txt

