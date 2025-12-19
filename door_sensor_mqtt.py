import RPi.GPIO as gpio
import paho.mqtt.client as paho
from time import sleep
import systemd_watchdog
import sys

def printDirect(message):
        print(message)
        sys.stdout.flush()

# Setup
klingel_gpio = 17 # GPIO of door contact.
polltime = 1.0

broker_ip = ""
broker_port = 1883
connect_timeout = 60
topic = "basement/door"
quality_of_service = 0 # 0: best effort 1: at least once 2: exactly once

printDirect('Started ...')
wd = systemd_watchdog.WatchDog()
if not wd.is_enabled:
    # Then it's probably not running as systemd with watchdog enabled
    raise Exception("Watchdog not enabled")

printDirect('Setup ... ')
gpio.setmode(gpio.BCM)
gpio.setup(klingel_gpio, gpio.IN, pull_up_down=gpio.PUD_UP)
client = paho.Client()
if client.connect(broker_ip, broker_port, connect_timeout) != 0:
        raise Exception('Could not connect to the mqtt broker!')
printDirect('Connected to broker ... ')
wd.ready()
wd.status("Connected to broker ...")
sentOnce = False
while True:
        sleep(polltime)
        wd.ping()
        if gpio.input(klingel_gpio):
                client.publish(topic, "OPEN", quality_of_service)
        else:
                client.publish(topic, "CLOSED", quality_of_service)
        if not sentOnce:
                printDirect('First message sent!')
                wd.status("First message sent!")
                sentOnce = True