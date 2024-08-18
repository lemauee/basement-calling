from pynng import Sub0
from pynng.exceptions import Timeout
from baresipy import BareSIP
from time import sleep
import sys

def printDirect(message):
        print(message)
        sys.stdout.flush()

DEFAULT_PUBLISHER_ADDRESS = ""
DEFAULT_RECIEVE_TIMEOUT = 60000 #ms
DEFAULT_MAX_BAD_MSGS = 10

def alarm_wrapper(alarm_fcn,hid):
    hid.set_alarm()
    while (not hid.get_reset_button()):
        if hid.get_alarm_enabled():
            alarm_fcn()
    hid.reset_alarm()

def alarm_common(alarm_fcn, hid, publisher_address=DEFAULT_PUBLISHER_ADDRESS, recieve_timeout=DEFAULT_RECIEVE_TIMEOUT, maxBadMsgs=DEFAULT_MAX_BAD_MSGS):
    printDirect('Started ... ')
    while True:
        printDirect('Connecting ... ')
        try:
            subscriber = Sub0(dial=publisher_address,topics=b"",recv_timeout=recieve_timeout, recv_buffer_size=1)
            printDirect("Subscribed!")
            recievedOnce = False
            badMsgs = 0
            while True:
                try:
                    hid.read_input()
                    msg = subscriber.recv()
                    hid.heartbeat()
                    if msg == b"ALARM":
                        printDirect('Alarm due to not OK message!')
                        alarm_wrapper(alarm_fcn,hid)
                    elif msg != b'OK':
                        printDirect(f'Corrupted message \"{msg}\" recieved!')
                        badMsgs += 1
                        if badMsgs > maxBadMsgs:
                            printDirect('Alarm due to too many corrupted messages!')
                            alarm_wrapper(alarm_fcn,hid)
                    else:
                        badMsgs = 0
                        if not recievedOnce:
                            printDirect('First OK message recieved!')
                            recievedOnce = True
                except Timeout:
                    printDirect('Alarm due to recieve timeout!')
                    alarm_wrapper(alarm_fcn,hid)
                    recievedOnce = False

        except Exception as e:
                printDirect("Ran into exception in main loop: ")
                printDirect(e)
                alarm_wrapper(alarm_fcn,hid)
                printDirect("Sleep for a sec ...")
                sleep(1.0)
                printDirect("Reinitializing ...")


