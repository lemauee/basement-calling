import RPi.GPIO as gpio
from pynng import Pub0
from time import sleep
import sys

def printDirect(message):
        print(message)
        sys.stdout.flush()

# Setup
klingel_gpio = 4 # GPIO of door contact.
polltime = 0.1
open_time_threshold = 3.0

address = "tcp://basementip:13132"

printDirect('Started ... ')
while True:
        try:
                printDirect('Setup ... ')
                current_open_time = 0.0
                gpio.setmode(gpio.BCM)
                gpio.setup(klingel_gpio, gpio.IN, pull_up_down=gpio.PUD_UP)
                publisher = Pub0(listen=address)
                printDirect('Listening ... ')
                sentOnce = False
                while True:
                        sleep(polltime)
                        if gpio.input(klingel_gpio):
                                current_open_time += polltime
                                if current_open_time > open_time_threshold:
                                        printDirect("Alarm triggered!")
                                        publisher.send(b"ALARM")
                                        continue
                        else:
                                current_open_time = 0.0
                        publisher.send(b"OK")
                        if not sentOnce:
                                printDirect('First message sent!')
                                sentOnce = True
        except Exception as e:
                printDirect("Ran into exception: ")
                printDirect(e)
                printDirect("Sleep for a sec ...")
                sleep(1.0)
                printDirect("Reinitializing ...")
