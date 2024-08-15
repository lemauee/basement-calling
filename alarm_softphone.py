from pynng import Sub0
from pynng.exceptions import Timeout
from baresipy import BareSIP
from time import sleep
import sys

def printDirect(message):
        print(message)
        sys.stdout.flush()

# Setup
to = "**9" # Call all connected Phones.
gateway = "fritz.box"
user = ""
pswd = ""

address = "tcp://basementip:13132"
timeout = 60000 #ms
maxBadMsgs = 10

def alarm_call():
    try:
        printDirect("Alarm call!")
        b = BareSIP(user, pswd, gateway)
        b.call(to)
        while b.running:
                sleep(0.5)
                if b.call_established:
                        b.speak("alarm triggered")
                        b.hang()
                        b.quit()
                elif b.call_status == "DISCONNECTED":
                        printDirect("Phone not reachable!")
                        b.hang()
                        b.quit()
    except Exception as e:
        printDirect("Ran into exception while calling: ")
        printDirect(e)
        b.quit()

printDirect('Started ... ')
while True:
    printDirect('Connecting ... ')
    try:
        subscriber = Sub0(dial=address,topics=b"",recv_timeout=timeout,reconnect_time_min=timeout,reconnect_time_max=timeout, recv_buffer_size=1)
        printDirect("Subscribed!")
        recievedOnce = False
        badMsgs = 0
        while True:
            try:
                msg = subscriber.recv()
                if msg == b"ALARM":
                    printDirect('Alarm due to not ALARM message!')
                    alarm_call()
                elif msg != b'OK':
                    printDirect(f'Corrupted message \"{msg}\" recieved!')
                    badMsgs += 1
                    if badMsgs > maxBadMsgs:
                        printDirect('Alarm due to too many corrupted messages!')
                        alarm_call()
                else:
                    badMsgs = 0
                    if not recievedOnce:
                        printDirect('First OK message recieved!')
                        recievedOnce = True
            except Timeout:
                printDirect('Alarm due to recieve timeout!')
                alarm_call()
                recievedOnce = False

    except Exception as e:
            printDirect("Ran into exception in main loop: ")
            printDirect(e)
            alarm_call()
            printDirect("Sleep for a sec ...")
            sleep(1.0)
            printDirect("Reinitializing ...")


