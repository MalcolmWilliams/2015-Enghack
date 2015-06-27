import serial
import time

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
startSerial(ser, "COM18")

f = open("output.txt", "r")


''' example usage '''

while(1):

	while 1:
		temp = f.readline()
		#sendSerial(ser, temp)
		ser.write("g " + temp)
		time.sleep(0.001)
		if(ser.inWaiting() != 0):
			print "rx:", readSerial(ser)

	'''
	sendSerial(ser, ["1", "2", "3", "4"])

	

ser.close()
'''