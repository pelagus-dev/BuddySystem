import time
#import l76x
import math
from machine import UART, Pin
import gnss as g
from sx1262 import SX1262

print("buh1")


sx = SX1262(spi_bus=1, clk=10, mosi=11, miso=12, cs=3, irq=20, rst=15, gpio=2)

# LoRa
sx.begin(freq=915, bw=250.0, sf=12, cr=8, syncWord=0x12,
         power=22, currentLimit=140.0, preambleLength=8,
         implicit=False, implicitLen=0xFF,
         crcOn=True, txIq=False, rxIq=False,
         tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True)

# FSK
##sx.beginFSK(freq=923, br=48.0, freqDev=50.0, rxBw=156.2, power=-5, currentLimit=60.0,
##            preambleLength=16, dataShaping=0.5, syncWord=[0x2D, 0x01], syncBitsLength=16,
##            addrFilter=SX126X_GFSK_ADDRESS_FILT_OFF, addr=0x00, crcLength=2, crcInitial=0x1D0F, crcPolynomial=0x1021,
##            crcInverted=True, whiteningOn=True, whiteningInitial=0x0100,
##            fixedPacketLength=False, packetLength=0xFF, preambleDetectorLength=SX126X_GFSK_PREAMBLE_DETECT_16,
##            tcxoVoltage=1.6, useRegulatorLDO=False,
##            blocking=True)

while True:
    # get our own location
    pos = g.get_position()
    
    # rework function return into mathematically parsable content
    if (pos[0][0] == 'S'):
        pos[0][1] = -pos[0][1]
    
    if (pos[1][0] == 'W'):
        pos[1][1] = -pos[1][1]
    easy_pos = [pos[0][1], pos[1][1]]
    
    # serialise
    serial_pos = str(easy_pos[0]) + ',' + str(easy_pos[1])
    
    # turn into bytearray for OverTheAir transmission
    ota = str.encode(serial_pos)

    #print(easy_pos)
    #print(serial_pos)
    
    # send our own position back
    sx.send(ota)
    print(ota)
    print("Sent!!")

    msg, err = sx.recv()
    if len(msg) > 0:
        
        # parse other device's message
        error = SX1262.STATUS[err]
        print(f'received {msg}')
        print(error)
        
        msgtext = msg.decode()
        coords = msgtext.split(',')
        
        for i in range(len(coords)):
            coords[i] = float(coords[i])
        print(f'other device is at {coords}')
        
        # compute range
        distance = g.haversine(coords[1],coords[0],pos[1][1],pos[0][1])
        print(f'range: {1000*distance} metres')
        
        
    time.sleep(5)                   
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
