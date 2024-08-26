import RPi.GPIO as gpio
from time import sleep

from basement_calling import alarm_common
from basement_calling import alarm_hid

from schreihals_wiring import leds
from schreihals_wiring import buttons
from schreihals_wiring import siren

summer_gpio = siren.SIREN

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

hid = alarm_hid.AlarmHid(buttons.BTN_3, buttons.BTN_4, buttons.BTN_5, leds.SMALL_GREEN, leds.SMALL_YELLOW, leds.SMALL_RED)

alarm_common.alarm_common(alarm_summer, hid)