# Use to install influxdb on raspbian stretch

# The usual update and upgrade
apt -y update
apt -y upgrade

# Get repository key
wget -qO- https://repos.influxdata.com/influxdb.key | sudo apt-key add -

# Add repository to the sources list
echo "deb https://repos.influxdata.com/debian buster stable" | sudo tee /etc/apt/sources.list.d/influxdb.list

# Update again
apt -y update

# Install
apt -y install influxdb

