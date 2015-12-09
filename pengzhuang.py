# 多个文本文件两两碰撞相同内容
#-*- coding: cp936 -*-
import os,sys,glob,itertools
os.chdir(sys.path[0])

def getsame(a,b):
    la=[]
    lb=[]
    for i in open(a):
        la.append(i.strip())
    for i in open(b):
        lb.append(i.strip())
        
    ret =  list(set(la).intersection(set(lb)))  
    if len(ret)==0:
        return a[:-4]+'-'+b[:-4]+' : 匹配个数 0'
    else:
        return a[:-4]+'-'+b[:-4]+'  : 匹配个数 '+str(len(ret))+'\r\n'+' '.join(ret)+'\r\n'


fn=[]
for i in glob.glob('*.txt'):
    fn.append(i)


for a,b in itertools.combinations(fn,2):
    print getsame(a,b)