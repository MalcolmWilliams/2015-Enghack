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

serInput = serial.Serial()
startSerial(serInput, "COM20")

serOutput = serial.Serial()
startSerial(serOutput, "COM18")


#f = open("output.txt", "r")


''' example usage '''

while(1):

	while 1:
		#temp = f.readline()
		#sendSerial(ser, temp)
		
		#time.sleep(0.001)
		serInput.readline()		#should hold until new packet
		serInput.flushInput()
		#while(serInput.inWaiting() == 0):
		#	pass
			#time.sleep(0.0001)
		temp = serInput.readline()
		print temp
		serOutput.write("c " + temp)


	'''
	sendSerial(ser, ["1", "2", "3", "4"])

	

ser.close()
'''