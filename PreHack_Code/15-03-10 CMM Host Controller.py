'''
Test Algorithms for MTE201 Project: CMM

ALL MATH IN DEGREES
'''

import math
import time
import serial 
from Robot_Calculations import *


def cosLawGetSide(l1, l2, angle2):
	return math.sqrt(l1*l1 + l2*l2 - 2*l1*l2*math.cos(angle2) )

def cosLawGetAngle(l1, l2, l3):
	return math.acos( (l1*l1 + l2*l2 - l3*l3) / (2*l1*l2) )

def sinLawGetAngle(l2, l3, angle2):
	return math.asin(math.sin(angle2)/l3*l2)

#making the assumption that the arm never goes less then 90

#takes in angles, makes rads. calls cos, sin with rads
def getProbeCoords(length, angle):
	#print "angle:", angle
	for i in range(len(angle)):
		angle[i] = math.radians(angle[i])
	#print "R angle:", angle

	l3 = cosLawGetSide(length[1], length[2], angle[2])
	#print "l3", l3
	angle3 = sinLawGetAngle(length[2], l3, angle[2])
	#print "angle1:", math.degrees(angle[1]), "angle3:", math.degrees(angle3)
	hypXY = l3*math.cos(angle[1]-angle3)

	zPos = l3*math.sin(angle[1]-angle3)

	#print "hypXY", hypXY, "ZPos", zPos
	
	#if(angle[1]-angle3 < 0):
	#	zPos = -zPos
	
	zPos = zPos + length[0]

	yPos = hypXY * math.sin(math.pi - angle[0])
	xPos = hypXY * math.cos(math.pi - angle[0])


	return [xPos, yPos, zPos]

def getArmLengths(p, angles, baseHeight):
	#calulate the arm lengths given angles and effector coordinates
	project = []
	lengths = [0]*3
	project.append( math.sqrt( p[0]*p[0] - p[1]*p[1] ) )
	project.append( p[2] - baseHeight )

	l3 = math.hypot(project[0], project[1])
	#print 
	#print "l3:", l3
	#print "angles[1]:", math.degrees(angles[1])
	#print "proj 0:", project[0], ", 1:", project[1]
	#print "atan:", math.degrees(math.atan(project[0]/project[1]) )
	theta3 = angles[1] - ( -math.atan(project[0]/project[1]) + math.pi/2)
	theta4 = 2*math.pi - angles[2] - theta3

	#print "Theta3:", math.degrees(theta3)
	#print "Theta4:", math.degrees(theta4)

	ratio = l3/math.sin(angles[2])

	l1 = ratio * math.sin(theta4)
	l2 = ratio * math.sin(theta3)

	return [abs(l1), abs(l2)]


def getAngleError(length, point, angle):
	#point is the center of the bed (since it can be measured)
	bedCenter = [0, 105, 0]
	angleError = []

	#print "measured point:",
	#printPoint(point)

	angleError.append(abs(math.atan(point[0]/point[1])))

	if (point[0] < 0):
		angleError[0] = - angleError[0]

	l3 = math.hypot(point[0], point[1])

	#coslaw get angle(a,b,c) will return the angle c

	angleError.append( cosLawGetAngle(length[1], l3, length[2]) - angle[1] )

	angleError.append( cosLawGetAngle(length[1], length[2], l3) - angle[2] )

	for i in range(len(angleError)):
		angleError[i] = math.degrees(angleError[i])

	return angleError



def setTrim(trim, angleError):
	for i in range(len(trim)):
		trim[i] = trim[i] - angleError[i]



def cross(a, b):
	c =  [
		a[1] * b[2] - b[1] * a[2] ,
		a[2] * b[0] - b[2] * a[0] ,
		a[0] * b[1] - b[0] * a[1]
	]

	return c

def measureFourPoint(p):

	'''
	for i in range (len(p)):
		for j in range(len(p[0])):
			p[i][j] = float(p[i][j])
	'''
	#print "Have collected", len(p), "points:"
	
	#for i in range(len(p)):
#		printPoint(p[i])

	if(len(p) >= 4):
		#have enought data to calculate the distance
		planeVectors = []
		for i in range(2):
			temp = []
			for j in range(3):
				temp.append(p[0+i][j] - p[1+i][j])
			planeVectors.append(temp)
		#print planeVectors
		
		normal = cross(planeVectors[0], planeVectors[1])

		A = - sum( normal[i] * p[1][i] for i in range(3) )

		dist = ( sum (normal[j] * p[3][j] for j in range(3)) + A )  / math.sqrt(sum (normal[i]*normal[i] for i in range(3)))
		
		return abs(dist)

	else:
		return -1

def getSWEquations():
	f = open('equations.txt', 'r')
	output = []
	for i in range(6):
		temp = f.readline().replace("\n", "")
		temp = ''.join([c for c in temp if c in '1234567890.'])	#strip all non numeric chars
		output.append(float(temp))
	return output
	f.close()

#is unreliable (improper exception handling?)
def setSWEquations(lengths, angles):
	eqns = lengths
	for a in angles:
		eqns.append(a)


	eqnNames = ["LZero", "LOne", "LTwo", "ThetaZero", "ThetaOne", "ThetaTwo"]

	#use this syntax for better exception handling
	with open('equations.txt', 'w') as f:
		f.truncate(0)
		for i in range(6):
			f.write( '\"' + eqnNames[i] + '\"= ' + str(eqns[i]) + "\n" )
	f.closed


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
	for i in range(len(output)):
		output[i] = float(output[i])
	return output

def printPoint(p):
	print "%.4f \t %.4f \t %.4f" % (p[0], p[1], p[2])



def binarySearch(key, value):
	#always return index right before, or eaxct value
	#print value
	index = len(value)/2

	count = 1
	while(True):
		print "count:", count, "index:", index
		count += 1
		#assume it is within the range
		if(value[index] <= key and value[index + 1] > key):
			return index
		elif(value[index] < key):
			index = index + index/(2*count)
		else:
			index = index - index/(2*count)

def simpleSearch(key, value):
	found = False
	count = 1
	while(not found):
		if(value[count-1] <= key and value[count] > key):
			found = True
			return count -1
		count += 1

def interpolate(index, recordedResistance, angle, resistance):
	return angle[index+1] - ( (resistance[index+1]-recordedResistance) * (angle[index+1]-angle[index]) / (resistance[index+1]-resistance[index]) )
	


def readPotMapping():
	f = open("AngleDATA.txt", "r")
	#file is encoded as Angle, resistance0, resistance1, resistence2
	potMapping = [[] for i in range(4)]
	temp = f.readline()
	while(len(temp) != 0):
		temp = temp.replace("\n", "")
		temp = temp.replace("\t", " ")	#consider teh situation where the values are seperated by tabs
		temp = temp.split()

		#i want 4 columns, x rows
		for i in range(4):
			potMapping[i].append(float(temp[i]))

		temp = f.readline()
	f.close()
	return potMapping


def applyPotMapping(resistance, potMapping, trim,swapDirection):
	#take in a resistance per pot, massage them into angles (rad) by using offsets, lookuptables, interpolation

	angle = []
	for i in range(len(resistance)):
		#angle.append(interpolate( binarySearch(resistance[i], potMapping[i+1]), resistance[i], potMapping[0], potMapping[i + 1]) + trim[i])
		angle.append(interpolate( simpleSearch(resistance[i], potMapping[i+1]), resistance[i], potMapping[0], potMapping[i + 1]) + trim[i])
		if(swapDirection[i]):
			angle[i] = 180 - angle[i]
	return angle


#lengths = getSWEquations()[:3]
#angles = [0, 0, 0]	#init to 0
probeLocations = []

probeRadius = 2.38125 #in mm

measuringStrategy = "fourPoint"
distance = -1


ser = serial.Serial()
startSerial(ser, "COM11")


potMapping = readPotMapping()

'''
testpoints = [ [-22.41113914, -9.40079985, 23.55241371], 
			   [9.91502334, 40.36575344, 3.43557561], 
			   [31.64802526, -15.34273228, 2.56069417], 
			   [-9.286923, 3.97835671, -28.52794539] 
			   ]
'''
#desired distance with zero probe radius: 41.25964791

lengths = [54, 120, 148.6]
#angles = [90, 34.75, 113.44]
angles = [0, 0, 0]
#trim = [-104.36363636363637, -86.32070070967806, -96] #trim = [-103, -90, -90]
trim = [-103, -90, -90]
swapDirection = [False, True, True]

#probeCoords = [113.79559368413679, 0.0, 33.516731590858505]

#print "lengths:", lengths
#print "Angles:", angles
#print "probeCoords:", probeCoords

#print

#print "Calculated Probe Coords:", getProbeCoords( lengths, angles )
#print "Caluculated Arm lengths:", getArmLengths(probeCoords, angles, lengths[0])


#print potMapping

running = True
mode = 4 #0 for debug, 1 for distance, 2 for trangle calibration 

while running:
	if mode == 0:
	
		if(ser.inWaiting() != 0):
			angles = applyPotMapping(readSerial(ser), potMapping, trim, swapDirection)
			print "Angles:", angles
			coordinates = getProbeCoords(lengths, angles)
			print "coordinates:", coordinates
			#angleError =  getAngleError(lengths, coordinates, angles)
			#print "angle Error:", angleError
			#setTrim(trim, angleError)
			#print "Trim:", trim
			print

	if mode == 1:
		count = 0
			#count += 1
		while(len(probeLocations) < 4):
			#print "Loop Count:", count

			
			if(ser.inWaiting() != 0):	#if the number of chars in the serial buffer is not 0
				
				angles = applyPotMapping(readSerial(ser), potMapping, trim, swapDirection)
				#print angles
				#print "Angles:", angles
				

				probeLocations.append( getProbeCoords(lengths, angles) )	#should be a 2d array	
				#print probeLocations


				if measuringStrategy == "fourPoint":
					distance = measureFourPoint(probeLocations)



			if(distance != -1):
				print "The distance is:", distance

			time.sleep(0.01)
		running = False

	if mode == 2:
		voltages = []
		coordiates = []
		count = 1
		while(running):
			if(ser.inWaiting() != 0):
				voltages = readSerial(ser)
				angles = applyPotMapping(voltages, potMapping, trim, swapDirection)
				coordinates = getProbeCoords(lengths, angles)

				printPoint(coordinates)

				if(count >=6):
					running = False
				count += 1

	if mode == 3:
		if(ser.inWaiting() != 0):
			angles = applyPotMapping(readSerial(ser), potMapping, trim, swapDirection)
			print "Angles:", angles
			coordinates = getProbeCoords(lengths, angles)
			print "coordinates:", coordinates
			angleError =  getAngleError(lengths, coordinates, angles)
			print "angle Error:", angleError
			setTrim(trim, angleError)
			print "Trim:", trim
			print
			running = False

	if mode == 4:
		count = 1
		#f = open("Experimental Data 2 inch.txt", "w")
		while(running):
			probeLocations = []	
			while(len(probeLocations) < 4):
				if(ser.inWaiting() != 0):						
					angles = applyPotMapping(readSerial(ser), potMapping, trim, swapDirection)
					probeLocations.append( getProbeCoords(lengths, angles) )
					
			distance = measureFourPoint(probeLocations)
			print distance
			#f.write(str(distance) + "\n")

			if(count >=5):
				running = False
			count += 1
		#f.close()

	if mode == 5:
		count = 0
		if(ser.inWaiting() != 0):

			print count
			count += 1
		if(count >= 2):
			running = False
		

		( (f/m)* (omega)/(s^2 + omega^2) ) / (s^2+2*c*w*s + w)  