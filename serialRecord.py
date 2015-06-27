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

def passThrough(array):
	if(not array[3] and not array[4]):
		return True
	else:
		return False

def recording(array):
	if(array[3] and not array[4]):
		return True
	else:
		return False

def playback(array):
	if(not array[3] and array[4]):
		return True
	else:
		return False

def ignore(array):
	if(array[3] and array[4]):
		return True
	else:
		return False


serInput = serial.Serial()
startSerial(serInput, "COM20")

serOutput = serial.Serial()
startSerial(serOutput, "COM18")

startNewRecord = True
startNewPlayback = True


while 1:
	
	serInput.readline()		#should hold until new packet
	serInput.flushInput()
	inputArray = readSerial(serInput);	#returns array
	print inputArray
	
	if passThrough(inputArray):
		serOutput.write("c", str(inputArray[0]), str(inputArray[1]), str(inputArray[2]), "\n")
	
	elif recording(inputArray):
		if startNewRecord:
			f = open("recording.txt", "w")
			startNewRecord = False
		serOutput.write("c", str(inputArray[0]), str(inputArray[1]), str(inputArray[2]), "\n")
		f.write("c", str(inputArray[0]), str(inputArray[1]), str(inputArray[2]), "\n")

	elif playback(inputArray):
		if startNewPlayback:
			startNewRecord = True
			f = open("recording.txt", "r")
		temp = f.readline()
		serOutput.write("c ", temp)	