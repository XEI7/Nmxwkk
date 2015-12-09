def transfun(s):
	
	s |= 0x6E
	s = s << 1
	s &= 0xD7
	s = s >> 1
	s ^= 0x2E
	return s
	
list=[]
for i in range(95, 95+26):
	j=transfun(i)
	list.append(chr(j))
	
print sorted(list)
