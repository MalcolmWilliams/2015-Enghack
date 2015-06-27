import math

def cosLawGetSide(l1, l2, angle2):
	return math.sqrt(l1*l1 + l2*l2 - 2*l1*l2*math.cos(angle2) )

def sinLawGetAngle(l2, l3, angle2):
	return math.asin(math.sin(angle2)/l3*l2)

#making the assumption that the arm never goes less then 90
def getProbeCoords(lenght, angle):
	print "angle:", angle
	for i in range(len(angle)):
		angle[i] = math.radians(angle[i])
	print "R angle:", angle

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