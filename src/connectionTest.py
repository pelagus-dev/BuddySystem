import time
import random
import math
from machine import UART, Pin

button = Pin(6, Pin.IN, Pin.PULL_UP)

omron1 = Pin(19, Pin.IN, Pin.PULL_UP)
omron2 = Pin(18, Pin.IN, Pin.PULL_UP)
omron4 = Pin(17, Pin.IN, Pin.PULL_UP)
omron8 = Pin(16, Pin.IN, Pin.PULL_UP)



while True:
    if (button.value() == 1):
        print("On\n")
    else:
        print("Off\n")

    # binary to decimal; Pico doesn't like PULL_DOWN so invert binary first
    value = (1- omron1.value()) + 2* (1- omron2.value()) + 4 * (1- omron4.value()) + 8 * (1- omron8.value())

    # you can't have a convoy of zero vehicles
    value = 1 if value == 0 else value
    print(f'{value}\n')
    time.sleep(1)