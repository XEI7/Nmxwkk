#!coding:utf-8

import urllib
import re
import sys

def showinfo():
	print "#########################################################"
	print "###                 ����ȡ�������                    ###"
	print "###  �÷���python geturl.py <�����ؼ���> <ץȡ��ҳ��> ###"
	print "###        ����python geturl.py dedecms:5.1 5         ###"
	print "###        by: ����         qq:770416751              ###"
	print "###        ����bug��email��    email:hycsxs@qq.com    ###"
	print "#########################################################"

def test():
	print "<h4><a href=\"(.*)\" target=\"_blank\""

def gethtml(url):
	page=urllib.urlopen(url)
	html=page.read()
	return html

def geturl(html):
	a="<h4><a href=\"(.*)\" target=\"_blank\""
	resp=re.findall(a,html)
	return resp

def main(keywords,pagenum):
	num=0
	for x in range(1,int(pagenum)+1):
		html=gethtml('http://zoomeye.scanv.com/search?q=' + keywords + '&p=' + pagenum)
		url=geturl(html)
		num+=len(url)
		for y in url:
			print y
	print "�ܹ�ץȡ��"+str(num)+"����ַ!"

if __name__ == "__main__":
	if len(sys.argv) == 3:
		keywords=sys.argv[1]
		pagenum=sys.argv[2]
		main(keywords,pagenum)
	elif len(sys.argv) == 2:
		if sys.argv[1]=="-h" or sys.argv[1]=="--help":
			showinfo()
		else:
			keywords=sys.argv[1]
			pagenum=3
			main(keywords,pagenum)
	else:
		showinfo()

