#boring host functions

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

	
	eqnNames = ["LZero", "LOne", "LTwo", "ThetaZero", "ThetaOne", "ThetaTwo"]

	#use this syntax for better exception handling
	with open('equations.txt', 'w') as f:
		f.truncate(0)
		for i in range(6):
			f.write( '\"' + eqnNames[i] + '\"= ' + str(eqns[i]) + "\n" )
	f.closed