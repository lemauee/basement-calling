from pynng import Sub0
from pynng.exceptions import Timeout
from baresipy import BareSIP
from time import sleep
import sys

from basement_calling import alarm_common

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

alarm_common.alarm_common(alarm_call)


