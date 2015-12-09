#coding=utf-8
# A aaaaa B aaaab C aaaba D aaabb E aabaa
# F aabab G aabba H aabbb I abaaa J abaab
# K ababa L ababb M abbaa N abbab O abbba
# P abbbb Q baaaa R baaab S baaba T baabb
# U babaa
# V babab W babba X babbb Y bbaaa Z bbaab
# 第二种方式
# a AAAAA g AABBA n ABBAA t BAABA
# b AAAAB h AABBB o ABBAB u-v BAABB
# c AAABA i-j ABAAA p ABBBA w BABAA
# d AAABB k ABAAB q ABBBB x BABAB
# e AABAA l ABABA r BAAAA y BABBA
# f AABAB m ABABB s BAAAB z BABBB
import re
key={'aaaaa':'A','aaaab':'B','aaaba':'C','aaabb':'D','aabaa':'E','aabab':'F','aabba':'G','aabbb':'H','abaaa':'I','abaab':'J','ababa':'K','ababb':'L','abbaa':'M','abbab':'N','abbba':'O','abbbb':'P','baaaa':'Q','baaab':'R','baaba':'S','baabb':'T','babaa':'U','babab':'V','babba':'W','babbb':'X','bbaaa':'Y','bbaab':'Z'}
def chose(one,two):
	c=""
	d=""
	if len(s)%5 == 0 and s.isalpha():
		for i in s:
			if i.islower():
				i=one
				c=c+i
			else:
				i=two
				c=c+i
		c=re.findall(r'(.{5})',c)
		for ba in c:
			d=d+str(key.get(ba))
		print d
	else:
		print "It's not Bacon"
s = raw_input('Please input str:').replace(' ','')
chose(one='a',two='b')
chose(one='b',two='a')