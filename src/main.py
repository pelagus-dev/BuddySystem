import time
import random
import math
from machine import UART, Pin, I2C
import gnss as g
import pack as pk
from sx1262 import SX1262
from pcf8574 import PCF8574
from hd44780 import HD44780
from lcd import LCD

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
                pos = g.get_position()
                if (pos[0][0] == 'S'):
                    pos[0][1] = -pos[0][1]
                
                if (pos[1][0] == 'W'):
                    pos[1][1] = -pos[1][1]
                distance = g.haversine(coords[1],coords[0],pos[1][1],pos[0][1])
                print(f'range: {1000*distance} metres')
                
                # only consider oncoming vehicles
                weloaded = 0
                print(f'"loaded: " {loaded} "weloaded:" {weloaded}')
                if ((loaded == 1 and weloaded == 0) or (loaded == 0 and weloaded == 1)):
                    if (rid not in register[0]):
                        register[0].append(vehlist[0])
                        register[1].append(distance)
                        register[2].append(vehlist)
                print(register)
            
            # SPHAGETTI CODE :D (select two closest vehicles)
            if (len(register[0]) > 1):
                c1, c2 = register[1].index(sorted(register[1])[0]), register[1].index(sorted(register[1])[1])
            else:
                c1 = 0
                c2 = 0

            for i in range(len(register[0])):
                if (not (i == c1 or i == c2)):
                    register[0].pop(i)
                    register[1].pop(i)
                    register[2].pop(i)
            
            for i in range(len(register[0])):
                if (register[2][i][4] == 1):
                    hvyStr = "HEAVY"
                elif (register[2][i][4] == 0):
                    hvyStr = "LIGHT"
                lcd.write_line(f'{str(register[2][i][5])} {hvyStr} @ {math.trunc(1000 * register[1][i])}m',i)
                time.sleep(2)

# startup the display!
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
pcf = PCF8574(i2c)
hd44780 = HD44780(pcf, num_lines=2, num_columns=16)
lcd = LCD(hd44780, pcf)
lcd.backlight_on()

sx = SX1262(spi_bus=1, clk=10, mosi=11, miso=12, cs=3, irq=20, rst=15, gpio=2)

# LoRa
sx.begin(freq=915, bw=250.0, sf=11, cr=8, syncWord=0x12,
         power=22, currentLimit=140.0, preambleLength=8,
         implicit=False, implicitLen=0xFF,
         crcOn=True, txIq=False, rxIq=False,
         tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True)

sx.setBlockingCallback(False, on_recv)

rid = random.randint(0,999)

lcd.write_line("Buddy System", 0)
lcd.write_line("Waiting for GPS",1)
pos = g.get_position()
lcd.write_line("", 0)
lcd.write_line("GPS Fix Acquired",1)
time.sleep(3)
lcd.write_line("", 1)

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
    lcd.write_line("Sent Position!",1)

    time.sleep(2)
    lcd.write_line("",1)
    time.sleep(8)              
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