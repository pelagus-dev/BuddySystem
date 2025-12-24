import time
import random
#import l76x
import math
from machine import UART, Pin
import gnss as g
from sx1262 import SX1262

buh = "Hello"
ota = str.encode(buh)
sx.send(ota)
time.sleep(10)