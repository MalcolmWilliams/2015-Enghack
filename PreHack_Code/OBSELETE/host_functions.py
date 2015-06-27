#boring host functions

import math
import serial

def cosLawGetAngle(l1, l2, l3):
	return math.acos( (l1*l1 + l2*l2 - l3*l3) / (2*l1*l2) )

print math.degrees( cosLawGetAngle(80.27, 81.76, 136.42) )