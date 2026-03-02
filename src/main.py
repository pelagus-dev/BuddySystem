import time
import random
import math
from machine import UART, Pin
import gnss as g
import pack as pk
from sx1262 import SX1262
import heapq

print("buh1")

# rids, last known distances, full vehlist
register = [[],[],[]]

def on_recv(events):
    if events & SX1262.RX_DONE:
        msg, err = sx.recv()
        if len(msg) > 0:
            
            # parse other device's message
            error = SX1262.STATUS[err]
            print(f'received {msg}')
            print(error)
            
            if (error == "ERR_NONE"):
                msgtext = msg.decode()
                vehlist = pk.unload(pk.extract(msgtext))
                rid, lat, lon, loaded, heavy, convoy_size = vehlist
                coords = [lat, lon]
                for i in range(len(coords)):
                    coords[i] = float(coords[i])
                print(f'other device is at {coords}')
                distance = g.haversine(coords[1],coords[0],pos[1][1],pos[0][1])
                print(f'range: {1000*distance} metres')

                # only consider oncoming vehicles
                if (loaded == 1 and weloaded == 0 or loaded == 0 and weloaded == 1):
                    if (rid not in register[0]):
                        register[0].append(vehlist[0])
                        register[1].append(distance)
                        register[2].append(vehlist)

            # SPHAGETTI CODE :D (select two closest vehicles)
            c1, c2 = register[1].index(heapq.nsmallest(2,register[1])[0]), register[1].index(heapq.nsmallest(2,register[1])[1])

            for i in range(len(register[0])):
                if (not (i == c1 or i == c2)):
                    register[0].pop(i)
                    register[1].pop(i)
                    register[2].pop(i)
            
            for i in range(len(register[0])):
                if (register[2][i][4] == 1):
                    hvyStr = "HVY"
                elif (register[2][i][4] == 0):
                    hvyStr = "LGT"
                print(f'{str(register[2][i][5])} {hvyStr} @ {register[0][i]}m')
                

sx = SX1262(spi_bus=1, clk=10, mosi=11, miso=12, cs=3, irq=20, rst=15, gpio=2)

# LoRa
sx.begin(freq=915, bw=250.0, sf=11, cr=8, syncWord=0x12,
         power=22, currentLimit=140.0, preambleLength=8,
         implicit=False, implicitLen=0xFF,
         crcOn=True, txIq=False, rxIq=False,
         tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True)

sx.setBlockingCallback(False, on_recv)

rid = random.randint(0,999)

while True:
    weloaded = 1
    weheavy = 0
    convoy_size = 2

    # get our own location
    pos = g.get_position()
    
    # rework function return into mathematically parsable content
    if (pos[0][0] == 'S'):
        pos[0][1] = -pos[0][1]
    
    if (pos[1][0] == 'W'):
        pos[1][1] = -pos[1][1]
    easy_pos = [pos[0][1], pos[1][1]]
    
    transmission_list = [rid, easy_pos[0], easy_pos[1], weloaded, weheavy, convoy_size]
    serialized = pk.compress(pk.load(transmission_list))
    
    # turn into bytearray for OverTheAir transmission
    ota = str.encode(serialized)
    
    # send our own position
    sx.send(ota)
    print(ota)
    print("Sent!!")
    
    time.sleep(10)                   
'''
x=l76x.L76X()
x.L76X_Set_Baudrate(9600)
x.L76X_Send_Command(x.SET_NMEA_BAUDRATE_115200)
time.sleep(2)
x.L76X_Set_Baudrate(115200)

x.L76X_Send_Command(x.SET_POS_FIX_400MS);

#Set output message
x.L76X_Send_Command(x.SET_NMEA_OUTPUT);

time.sleep(2)
x.L76X_Exit_BackupMode();
x.L76X_Send_Command(x.SET_SYNC_PPS_NMEA_ON)

#x.L76X_Send_Command(x.SET_STANDBY_MODE)
#time.sleep(10)
#x.L76X_Send_Command(x.SET_NORMAL_MODE)
#x.config.StandBy.value(1)

while(1):
    RSTime, RSLattitude, RSLongtitude, RSGroundSpeed, RSDirection, RSDate, RSVariation = x.L76X_Gat_GNRMC()
    print("hi??")
    print ("Time : ", RSTime)
    print ("Lattitude : ", RSLattitude)
    print ("Longtitude : ", RSLongtitude)
    print ("Ground speed in knots : ", RSGroundSpeed)
    print ("Compass direction : ", RSDirection)
    print ("Today's date : ", RSDate)
    print ("Magnetic Variation : ", RSVariation)
    print ("--------------------------------------------")
    time.sleep(5)
'''