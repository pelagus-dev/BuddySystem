import time
import random
#import l76x
import math
from machine import UART, Pin
import gnss as g
from sx1262 import SX1262

msg, err = sx.recv()
error = SX1262.STATUS[err].decode()
message = msg.decode()

obled = machine.Pin("LED", machine.Pin.OUT)

if (message == "Hello" and error == "ERR_NONE"):
    obled.value(1)
    time.sleep(0.2)
    obled.value(0)
    obled.value(1)
    time.sleep(0.2)
    obled.value(0)
    obled.value(1)
    time.sleep(0.2)
    obled.value(0)
    obled.value(1)
    time.sleep(0.2)
    obled.value(0)
elif (message == "Hello" and error):
    obled.value(1)
    time.sleep(0.2)
    obled.value(0)
    obled.value(1)
    time.sleep(0.2)
    obled.value(0)
elif (message):
    obled.value(1)
    time.sleep(0.2)
    obled.value(0)