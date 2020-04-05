# Start grafana server
sudo systemctl start grafana-server
# Start influxdb database
sudo systemctl start influxdb

# Start python program
nohup python3 weatherstation.py > weatherstation.log 2>&1 &

