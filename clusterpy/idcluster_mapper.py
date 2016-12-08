import sys
import re

"""
file_d=open('dd','r')

for line in file_d:
	line=line.strip()
	line=re.sub('\[|\]|\'|\s','',line)
	ts=line.split(',')
	for t in ts:
		if not t:
			break
		print t,'\t',line
"""

p=re.compile(';')

for line in sys.stdin:
	line=line.strip()
	ts=line.split('\t')
	if len(ts)!=4:
		break
	sum_weight=ts[0]
	num_id=ts[1]
	avr_weight=ts[2]
	ids=p.split(ts[3])
	for x in ids:
		if not x:
			break
		sys.stdout.write('%s\t%s\t%s\t%s\t%s\n'%(x,sum_weight,num_id,avr_weight,ts[3]))
