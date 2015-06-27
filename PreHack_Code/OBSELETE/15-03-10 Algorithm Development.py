'''
Test Algorithms for MTE201 Project: CMM

ALL MATH IN RADIANS
'''

import math
import time
import serial

def startSerial(ser, port):
	ser.baudrate = 9600
	ser.port = port
	ser.timeout = 20
	ser.open()
	ser.flushInput()
	print "Serial Settings: " + str(ser)
	print "Prepared To Start Communication"


def cosLawGetSide(l1, l2, angle2):
	return math.sqrt(l1*l1 + l2*l2 - 2*l1*l2*math.cos(angle2) )

def sinLawGetAngle(l2, l3, angle2):
	return math.asin(math.sin(angle2)/l3*l2)

#making the assumption that the arm never goes less then 90
def getProbeCoords(lenght, angle):
	#can be much more efficient
	l3 = cosLawGetSide(lenght[1], lenght[2], angle[2])
	angle3 = sinLawGetAngle(lenght[2], l3, angle[2])
	xPos = l3*math.cos(angle[1]-angle3)
	zPos = l3*math.sin(angle[1]-angle3)
	if(angle[1]-angle3 < 0):
		zPos = -zPos
	zPos = zPos + lenght[0]

	#rotate plane
	xPos = xPos * math.cos(angle[0]-math.pi/2)
	yPos = xPos * math.sin(angle[0]-math.pi/2)
	if(angle[0]-math.pi/2 < 0):
		xPos = -xPos
		yPos = -yPos

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


def readSerial(ser):
	temp = ser.readline()
	temp = temp.replace("\n", "")	#strip the newline char
	output = temp.split() 	#splits the string.
	for i in range(len(output)):
		output[i] = float(output[i]) 
	return output

def printPoint(p):
	print "X = %.4f Y = %.4f Z = %.4f" % (p[0], p[1], p[2])

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
	print "Have collected", len(p), "points:"
	
	for i in range(len(p)):
		printPoint(p[i])

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

def binarySearch(key, values):
	#always return index right before, or eaxct value
	index = len(values)/2

	while(True):
		#assume it is within the range
		if(value[index] <= key and value[index + 1] > key):
			return index
		else if(value[index] > key):
			index = index + index/2
		else:
			index = index - index/2

def interpolate(index, recordedResistance, angle, resistance):
	return angle[index+1] - ( (resistance[index+1]-recordedResistance) * (angle[index+1]-angle[index]) / (resistance[index+1]-resistance[index]) )

def readPotMapping():
	f = open("AngleDATA.txt", "r")
	#file is encoded as Angle, resistance0, resistance1, resistence2
	potMapping = []
	temp = f.readline()
	while(len(temp) != 0):
		temp = temp.replace("\n", "")
		temp = temp.replace("\t", " ")	#consider teh situation where the values are seperated by tabs
		temp = temp.split()

		potMapping.append(temp)

	return potMapping


def applyPotMapping(resistance, potMapping):
	#take in a resistance per pot, massage them into angles (rad) by using offsets, lookuptables, interpolation

	trim = [0, 0, 0]	#trim in rads for each arm

	angle = []
	for i in range(len(resistance)):
		angle.append(interpolate( binarySearch(resistance[i], potMapping[0]), resistence[i], potMapping[i + 0]) + trim[i])

	return angle
#lengths = getSWEquations()[:3]
#angles = [0, 0, 0]	#init to 0
probeLocations = []

probeRadius = 2.38125 #in mm

measuringStrategy = "fourPoint"
distance = -1

ser = serial.Serial()
startSerial(ser, "COM5")

potMapping = readPotMapping()

'''
testpoints = [ [-22.41113914, -9.40079985, 23.55241371], 
			   [9.91502334, 40.36575344, 3.43557561], 
			   [31.64802526, -15.34273228, 2.56069417], 
			   [-9.286923, 3.97835671, -28.52794539] 
			   ]
#desired distance with zero probe radius: 41.25964791
'''
lengths = [26.82, 71.58, 64.7]
#angles = [math.radians(90), math.radians(34.75), math.radians(113.44)]
angles = [0, 0, 0]
#probeCoords = [113.79559368413679, 0.0, 33.516731590858505]

#print "Lenghts:", lengths
#print "Angles:", angles
#print "probeCoords:", probeCoords

#print

#print "Calculated Probe Coords:", getProbeCoords( lengths, angles )
#print "Caluculated Arm Lenghts:", getArmLengths(probeCoords, angles, lengths[0])

count = 0
while(len(probeLocations) < 4):
	#count += 1
	#print "Loop Count:", count


	if(ser.inWaiting() != 0):	#if the number of chars in the serial buffer is not 0
		
		angles = applyPotMapping(readSerial(ser))
		#print "Angles:", angles
		
		probeLocations.append( getProbeCoords(lengths, angles) )	#should be a 2d array	
		#print probeLocations	

		if measuringStrategy == "fourPoint":
			distance = measureFourPoint(probeLocations)

	if(distance != -1):
		print "The distance is:", distance

	time.sleep(0.01)