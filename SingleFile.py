import serial
import threading
from datetime import datetime
from threading import Timer


ser = serial.Serial('COM8', 38400, parity = serial.PARITY_NONE, stopbits = 1, bytesize = serial.EIGHTBITS)

msg = chr(27) + "040\n\r"
print(msg)
ser.write(msg.encode())

resp = ser.readline()
print(resp)

def sendmsg(cmdid):
    msg = chr(27) + cmdid + "\n\r"
    ser.write(msg.encode())
    return ser.readline()

import re
def readpwr():
    resp = sendmsg("047")
    return re.sub("[^\d\.]", "", str(resp))

 

def readDTSense():
    resp = sendmsg("04C")
    return re.sub("[^\d\.]", "", str(resp))
def readChiller():
    resp = sendmsg("04D")
    return re.sub("[^\d\.]", "", str(resp))
def readOPRRfreq():
    resp = sendmsg("04Z")
    return re.sub("[^\d\.]", "", str(resp))

 

def readandsave():
    now = datetime.now()
    timestamp = dt_string = now.strftime("%Y%m%d %H:%M:%S")
    pwr = readpwr()
    DT = readDTSense()
    Chiller = readChiller()
    OPRR = readOPRRfreq()
    with open("log.txt", "a") as datafile:
        datafile.write(timestamp + ", " + pwr + ", " + DT + ", " + Chiller + ", " + OPRR + "\n\r")
    print(timestamp + ", " + pwr + ", " + DT + ", " + Chiller + ", " + OPRR)

 

def printit():
  Timer(10.0, readandsave).start()

 


def update():
    import time
    while True:
        readandsave()
        time.sleep(10)
		
update()
