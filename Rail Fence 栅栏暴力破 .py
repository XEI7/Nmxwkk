#! coding: utf-8
def decode(text, num):
	ind = []
	for i in range(num):
		j=0
		while 1:
			if i+j*num>=len(text)-1:
				break
			ind.append(i+j*num)
			j+=1
	return ''.join([text[t] for t in ind])



str = "kyssmlxeei{ipeu}"+" "
for i in range(2,len(str)-1):
	print i,decode(str, i)
