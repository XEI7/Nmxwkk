__author__="F4nt45i4-ZHG"
from zlib import *
t = open('yes.png', 'rb').read()[0x57:-12]
i = 0
data = b''
while True:    
	if i >= len(t): break
	l = (ord(t[i]) << 24) + (ord(t[i + 1]) << 16) + (ord(t[i + 2]) << 8) + ord(t[i + 3])    
	i += 4    
	print(t[i:i+4])    
	i += 4    
	data += t[i:i+l]    
	i += l    
	i += 4
with open('160zlibd.txt', 'wb') as f:    
	f.write(decompress(data)) 
