#!/usr/bin/env python

#file_label=open('./newdata/opi.matrix.formated.rc.label.txt','r')
file_label=open('labels','r')
file_id=open('idcode','r')
file_name=open('./newdata/renren.userlist','r')

kv={}
for line in file_name:
	#name_line=unicode(line,'utf8')
	name_line=line
	idname=name_line[:-1].split('\t',2)
	#print idname[0]
	if kv.has_key(idname[0]):
		break;
	else:
		kv[idname[0]]=idname[1]
d={}

for line in file_label:
	id_line=file_id.readline()[:-1]
	userid=id_line.split('\t',2)[0]

	#label=line[:-2]
	label=line.strip()
	#print label
	if d.has_key(label):
		if kv.has_key(userid):
			d[label]=d[label]+'<'+kv[userid]+'_'+userid+'>'
		else:
			d[label]=d[label]+'<'+'XXX_'+userid+'>'
	else:
		if kv.has_key(userid):
			d[label]='<'+kv[userid]+'_'+userid+'>'
		else:
			d[label]='<XXX_'+userid+'>'

#print d
for (k,v) in d.items():
	#print type(v)
	#print k,'\t',v.encode('utf8')
	print k,'\t',v
	#pass
