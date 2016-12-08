#!/usr/bin/env python

import sys
idfile=open(sys.argv[1],'r')

userfile=open('./newdata/renren.userlist','r')

userdict={}
for line in userfile:
	line=line.strip()
	idname=line.split('\t')
	userdict[idname[0]]=idname[1]

#print userdict.keys()

i=0
for line in idfile:
	line=line.strip()
	ids=line.split(',')
	i+=1
	sys.stdout.write('%d\t'%i)
	for id in ids:
		if userdict.has_key(id):
			sys.stdout.write('<%s_%s>'%(userdict[id],id))
		else:
			sys.stdout.write('<XXX_%s>'%id)
	sys.stdout.write('\n')
