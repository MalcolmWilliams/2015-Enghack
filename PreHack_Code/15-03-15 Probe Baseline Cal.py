'''
Script for controlling the printer and getting a base calibration for the probe

attach the probe
probe 100 times, in the center
log
graph

'''


import serial

def startSerial(ser, port):
	ser.baudrate = 9600
	ser.port = port
	ser.timeout = 20
	ser.open()
	ser.flushInput()
	print "Serial Settings: " + str(ser)
	print "Prepared To Start Communication"

def log(f, iteration, distance):
	toWrite = str(iteration) + "\t" + str(distance) + "\n"
	print toWrite,
	f.write(toWrite)

def probe(ser):
	ser.write("G30\n")
		
	temp = ser.readline()
	temp = float(temp[2:9])
	ser.readline()		#this readline is to handle the "ok" response

	return temp

def home(ser):	
	ser.write("G28\n")
	ser.readline();

def goto (ser, xPos, yPos, zPos):
	probeX = -5.73
	probeY = 20.87
	cmd = "GO X" + str(xPos - probeX) + " Y" + str(yPos - probeY) + " Z" + str(zPos) + "\n"
	ser.write(cmd)
	ser.readline()



ser = serial.Serial()
startSerial(ser, "COM9")

home(ser)
goto(ser, 0, 0, 140)

logFile = open("45 deg angle.txt", "w")

for i in range(10):
	log(logFile, i , probe(ser))