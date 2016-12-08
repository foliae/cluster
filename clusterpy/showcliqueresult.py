#!/usr/bin/env python

import sys
#file_label=open('./newdata/opi.matrix.formated.rc.label.txt','r')
#file_name=open('./20100917/renren.userlist_','r')
#file_name=open('./20100917/renren.userlist','r')
file_name=open(sys.argv[1],'r')

kv={}
for line in file_name:
	#name_line=unicode(line,'utf8')
	#print line
	name_line=line.strip()
	idname=name_line.split('\t',2)
	#print idname[0]
	if len(idname)!=2:
		print 'userdict file format error:',idname
		continue
	if kv.has_key(idname[0]):
		continue;
	else:
		kv[idname[0]]=idname[1]

#exit()
for line in sys.stdin:

	line=line.strip()
	items=line.split('\t')

	"""
	if len(items)!=5:
		break
	if not kv.has_key(items[0]):
		continue
	"""

	members=items[-1].split(';')

	#sys.stdout.write('<'+kv[items[0]]+'_'+items[0]+'>\t')
	sys.stdout.write(items[0]+'\t')
	for m in members:
		if not m:
			break
		if kv.has_key(m):
			sys.stdout.write('<'+kv[m]+'_'+m+'>')
		else:
			sys.stdout.write('<'+'XXX_'+m+'>')
	
	sys.stdout.write('\n')

