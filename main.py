import time
import RPi.GPIO as gpio
from baresipy import BareSIP
from time import sleep

# Setup
klingel_gpio = 4 # GPIO of door contact.
to = "**9" # Call all connected Phones.
gateway = "fritz.box"
user = ""
pswd = ""
polltime = 0.1
open_time_threshold = 3.0

current_open_time = 0.0
gpio.setmode(gpio.BCM)
gpio.setup(klingel_gpio, gpio.IN, pull_up_down=gpio.PUD_UP)
while True:
        sleep(polltime)
        if gpio.input(klingel_gpio):
                current_open_time += polltime
                if current_open_time > open_time_threshold:
                        print("Alarm triggered!")
                        try:
                                b = BareSIP(user, pswd, gateway)
                                b.call(to)
                                while b.running:
                                        sleep(0.5)
                                        if b.call_established:
                                                b.speak("alarm triggered")
                                                b.hang()
                                                b.quit()
                                        elif b.call_status == "DISCONNECTED":
                                                print("Phone not reachable!")
                                                b.hang()
                                                b.quit()
                        except:
                                print("Ërror while calling!")
                                b.quit()
                        current_open_time = 0.0
