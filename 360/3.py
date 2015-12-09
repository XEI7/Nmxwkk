__author__="F4nt45i4-ZHG"
import numpy
A = []
with open('s2.txt', 'rb') as reader:
    data = reader.read()
    for i in range(96):
            A.append([])
            for j in range(96): 
            	part = data[:4]
            	data = data[4:] 
            	num = ord(part[0]) + (ord(part[1])<<8) + (ord(part[2])<<16) + (ord(part[3])<<24)
            	A[i].append(num)
A = numpy.array(A)
b = []
with open('s1.txt', 'rb') as reader:
	data = reader.read() 
	for i in range(96):
		part = data[:4] 
		data = data[4:]
		num = ord(part[0]) + (ord(part[1])<<8) + (ord(part[2])<<16) + (ord(part[3])<<24) 
		b.append(num)
b = numpy.array(b)
x = numpy.linalg.solve(A, b)
s = ''.join(map(lambda x: chr(int(round(x))), x))
print(s) 
