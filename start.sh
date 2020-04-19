# Start grafana server
systemctl start grafana-server
# Start influxdb database
systemctl start influxdb
# Start telegraf service
systemctl start telegraf

# Start python program
#nohup python3 weatherstation.py > weatherstation.log 2>&1 &
nohup python3 weatherstation.py > /dev/null 2>&1 &
