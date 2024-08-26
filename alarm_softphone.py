from pynng import Sub0
from pynng.exceptions import Timeout
from baresipy import BareSIP
from time import sleep
import sys

from basement_calling import alarm_common
from basement_calling import alarm_hid

from schreihals_wiring import leds
from schreihals_wiring import buttons

def alarm_call():
    to = "**9" # Call all connected Phones.
    gateway = "fritz.box"
    user = ""
    pswd = ""
    try:
        alarm_common.printDirect("Alarm call!")
        b = BareSIP(user, pswd, gateway)
        b.call(to)
        while b.running:
                sleep(0.5)
                if b.call_established:
                        b.speak("alarm triggered")
                        b.hang()
                        b.quit()
                elif b.call_status == "DISCONNECTED":
                        alarm_common.printDirect("Phone not reachable!")
                        b.hang()
                        b.quit()
    except Exception as e:
        alarm_common.printDirect("Ran into exception while calling: ")
        alarm_common.printDirect(e)
        b.quit()

hid = alarm_hid.AlarmHid(buttons.BTN_0, buttons.BTN_1, buttons.BTN_2, leds.BIG_GREEN, leds.BIG_YELLOW, leds.BIG_RED)

alarm_common.alarm_common(alarm_call, hid)


