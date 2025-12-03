import time
#import l76x
import math
from machine import UART, Pin
from math import radians, cos, sin, asin, sqrt

def get_position():
    uart_print = UART(0,baudrate=9600,tx=Pin(0),rx=Pin(1))
    #uart_print = UART(1,baudrate=9600,tx=Pin(4),rx=Pin(5))
    StandBy = Pin(17,Pin.OUT)
    StandBy.value(0)
    ForceOn = Pin(14,Pin.OUT)
    ForceOn.value(0)
    recv = bytes()
    while True:
        try:
            if uart_print.any() > 0:
                recv = uart_print.read(2048)
                #print(recv)
            uart_string = recv.decode('utf-8')
            #if uart_string:
                #print(uart_string)
            string_length = len(uart_string)
            if (uart_string.find("$GNGGA") >-1):
                start_point = uart_string.index("$GNGGA")+7
                end_point = uart_string.index("M")
                uart_string = uart_string[start_point : end_point]
                nmea_list = uart_string.split(',')
                
                if (nmea_list[1] and nmea_list[2] and nmea_list[3] and nmea_list[4]):
                    lat = nmea_list[1]
                    lat_quadrant = nmea_list[2]
                    lon = nmea_list[3]
                    lon_quadrant = nmea_list[4]
                    
                    # Good ol' foul one-liner that splits strings, converts types, converts DDM to DD, and builds a pretty little 2D array
                    coordinates = [lat_quadrant,(int(lat[0:2])+float(lat[3:])/60)],[lon_quadrant,(int(lon[0:3])+float(lon[4:])/60)]
                    if lat and lon:
                        #print(coordinates)
                        print(f'\nYOU ARE AT {coordinates[0][0]} {coordinates[0][1]}, {coordinates[1][0]} {coordinates[1][1]}\n')
                        break
                    else:
                        print("Waiting for fix...")

        except UnicodeError:
            continue
    return coordinates

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r
