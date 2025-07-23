# basement-calling
Simple basement alarm system for Raspberry PI (5) reporting a door status via MQTT.

# Hardware

## Required
* Raspi 5 - similar "Credit card computers" should work too
* (Magnet Switch) Contact closing when door is closed - Connected between Ground and the selected GPIO set to pull up

## Recommended
* Wired Connection Between Raspi and the Fritz Box (or a similar SIP server) - Powerline LAN worked for me

# Setup
## Raspbian convenience
* Enable SSH + create user already during card flashing.
* I used Raspbian Bookworm (May 2024).

## System dependencies
### Pip
`sudo apt-get install python3-pip`

### Paho MQTT
`sudo apt install python3-paho-mqtt`

### Install systemd-watchdog
`pip install --break-system-packages systemd-watchdog`

## Copy door_sensor_mqtt.py somewhere reasonnable
E.g. your home.

## Insert your mqtt broker IP into the respective line in main.py
`broker_ip=""`

## Make it executeable
`sudo chmod +x door_sensor_mqtt.py`

## systemd for autostart - door_sensor_mqtt.service
Change `User=` to your username set up on the raspi. Also change `WorkingDirectory=` to your users home.
Change the path in ExecStart to `/home/USER/main.py`.

Copy `door_sensor_mqtt.service` to `/etc/systemd/system/`. (Or create the file anew using `sudo nano /etc/systemd/system/door_sensor_mqtt.service`)

Change the file permissions `sudo chmod 644 /etc/systemd/system/door_sensor_mqtt.service`

Reload systemd to index the new service `sudo systemctl daemon-reload`

Enable the new service on startup `sudo systemctl enable door_sensor_mqtt.service`

Start it right now `sudo systemctl enable door_sensor_mqtt.service`

### Get logs
`sudo journalctl -u door_sensor_mqtt.service`

# Dealing with the Raspi remotely
## Reboot
`sudo shutdown -r now`
## Check if our app is running
`ps -ef | grep python`

