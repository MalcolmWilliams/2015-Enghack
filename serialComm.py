# python import test
#import serial 

'''

Discov3ry Standalone GUI

Simple Python GUI to control the Discov3ry paste extruder.

Created by Malcolm Williams
Date June 8th 2015

'''

import serial
import easygui
import datetime


def startSerial(ser, port):
	ser.baudrate = 9600
	ser.port = port
	ser.timeout = 20
	ser.open()
	ser.flushInput()
	print "Serial Settings: " + str(ser)
	print "Prepared To Start Communication"


def readSerial(ser):
	temp = ser.readline()
	temp = temp.replace("\n", "")	#strip the newline char
	output = temp.split() 	#splits the string.
	#for i in range(len(output)):
		
		#output[i] = float(output[i])
	return output

def sendSerial(ser, array):
	toSend = "g "
	for a in array:
		toSend = toSend + a + " "
	ser.write(toSend + "\n")
	#print "tx:", toSend

ser = serial.Serial()
startSerial(ser, "COM17")


while(1):
	sendSerial(ser, ["1", "2", "3", "4"])

	if(ser.inWaiting() != 0):
		print "rx:", readSerial(ser)

ser.close()

'''

filename = "fifo.tmp"



# Block until writer finishes...
with open(filename, 'r') as f:
    data = f.read()

# Split data into an array
array = [int(x) for x in data.split()]

print array

'''