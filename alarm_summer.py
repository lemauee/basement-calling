import RPi.GPIO as gpio
from time import sleep

from basement_calling import alarm_common
from basement_calling import alarm_hid

summer_gpio = 4

gpio.setmode(gpio.BCM)
gpio.setup(summer_gpio, gpio.OUT)
print('Low')
gpio.output(summer_gpio, gpio.LOW)

def alarm_summer():
    print('Beep')
    gpio.output(summer_gpio, gpio.HIGH)
    sleep(1.0)
    gpio.output(summer_gpio, gpio.LOW)
    sleep(1.0)

hid = alarm_hid.AlarmHid(, , , , , )

alarm_common.alarm_common(alarm_summer, hid)