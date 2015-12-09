# -*- coding: gb18030 -*-
from subprocess import  *
import socket,httplib2
import sys,os,socket,threading
from bs34 import BeautifulSoup34
import json,urllib2,urllib
from urlparse import urlparse as up
import simplejson,pprint


class target(object):
    def __init__(self,domain):
        self.domain=domain
        self.ips=[]
        self.subdomain=[]
        self.ipinfo=[]
        self.iprinfo=[]
        self.samesite=[]
        self.url=r'http://cn.bing.com/search?count=100&q=ip:'
        self.subdomainurl=r'https://ajax.googleapis.com/ajax/services/search/web?v=1.0&start={}&rsz=8&q=site:{}'
        self.httphead={
        'User-Agent':'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; User-agent: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; http://bsalsa.com) ; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152)',
        'Cookie':'SRCHUID=V=2&GUID=79E9F92F75B54E60B4588D130264EFD4; MUID=0A81369FC80C6E532B69359EC9026E42; SRCHD=SM=1&MS=2196069&D=2160426&AF=NOFORM; SRCHUSR=AUTOREDIR=0&GEOVAR=&DOB=20120209; _SS=SID=C8C39DCC3EA342E2859C472E445A1BEC; _UR=D=0; RMS=F=O&A=Q; SCRHDN=ASD=0&DURL=#',
        'Referer':'http://cn.bing.com/'}
        self.portlist=[21,22,23,25,53,80,81,110,139,135,443,445,1723,2012,3389,1433,3306,1521,8080,8089,8090,3128,5900]
        self.op=[]
        self.ipq=r'http://api.ipinfodb.com//v2/ip_query.php?key=5eb5b4de91741e2e4b98748989dc84f3236b55f6dd38aa689921884867536f36&ip={}&output=json&timezone=false'
        self.getips()
        self.trac()
        self.scanport()
        self.getsubdomain()
        self.getpzinfo()
        self.disp()

#--------------------------------获得ip,srver 信息----------------------------
    def getips(self):
        h=httplib2.Http()
        res,_=h.request(r'http://'+self.domain,headers=self.httphead)
        _,con=h.request(self.ipq.format(self.domain))
        con=json.loads(con)
        for i in socket.gethostbyname_ex(self.domain)[2]:
            self.ips.append(i)
        self.ipinfo.append((res.get('server'),res.get('x-powered-by'),con.get("CountryName"),con.get("RegionName"),con.get("City")))
            
#--------------------------------路由跟踪代码----------------------------
    def trac(self):
        p=Popen(['tracert',self.domain,'-h','20',],shell=False,stdout=PIPE)
        data=p.stdout.readline()
        while data:
            #if "*" in data:break
            d=data.strip().split()
            if len(d)==8:self.iprinfo.append((d[7],d[7]))
            if len(d)==9:self.iprinfo.append((d[7],d[8][1:-1]))
            data=p.stdout.readline()

#--------------------------------获得目标子域信息--------------------------
    def getsubdomain(self):
        for n in range(1,200,8):
            request = urllib2.Request(self.subdomainurl.format(n,self.domain[self.domain.index('.')+1:]), None, {'Referer': 'http://www.baidu.com'})
            try:info=simplejson.load(urllib2.urlopen(request))['responseData']['results']
            except Exception as err:break
            for i in info:
                for l in i:
                    if l=='url':
                        self.subdomain.append( up(i[l]).netloc.encode() )
            self.subdomain=list(set(self.subdomain))
#--------------------------------胖猪代码----------------------------
    def getpzinfo(self):
        ip=socket.gethostbyname(self.domain.strip())
        h=httplib2.Http()
        res,cont=h.request(self.url+ip,headers=self.httphead)
        soup=BeautifulSoup(cont)
        for i in soup.findAll('div',attrs={'class':'sb_tlst'}):
            self.samesite.append(up(i.a['href']).netloc.encode())
        self.samesite=list(set(self.samesite))

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#---------------------------端口扫描代码-------------------------------


    def conport(self,tar,port):
        s=socket.socket()
        s.settimeout(3)
        try:s.connect((tar,port));self.op.append(port)
        except Exception as err:pass
        finally:s.close()

    def scanport(self):
        tlist=[]
        for i in self.portlist:
            for l in self.ips:
                tlist.append(threading.Thread(target=self.conport,args=((l,i))))
        for i in tlist:
            i.start()
        for i in tlist:
            i.join()
        del tlist
    def disp(self):
        f=open(r'./txt/'+self.domain+'.txt','at')
        print >>f,"目标域名：\n",self.domain
        print "目标域名：\n",self.domain
        if len(self.samesite)>1:
            print >>f,"目标为虚拟主机"
            print "目标为虚拟主机"
        
        print >>f,"IP地址 :"
        pprint.pprint (self.ips,f)
        print "IP地址 :"
        pprint.pprint (self.ips)
        print >>f,"目标地址信息: "
        pprint.pprint (self.ipinfo,f)
        print "目标地址信息: "
        pprint.pprint (self.ipinfo)
        print >>f,"目标路由跟踪信息: "
        pprint.pprint (self.iprinfo,f)
        print "目标路由跟踪信息: "
        pprint.pprint (self.iprinfo)
        print >>f,"目标的开放端口信息: "
        pprint.pprint (self.op,f)
        print "目标的开放端口信息: "
        pprint.pprint (self.op)
        print >>f,"目标的子域信息："
        pprint.pprint (self.subdomain,f)
        print "目标的子域信息："
        pprint.pprint (self.subdomain)
        print >>f,"目标的同站服务器信息："
        pprint.pprint (self.samesite,f)
        print "目标的同站服务器信息："
        pprint.pprint (self.samesite)
        print >>f,"*"*30+'\r\n\r\n'
        print "*"*30+'\r\n\r\n'