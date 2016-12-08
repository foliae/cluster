#/usr/bin/env python

import sys
import os

curID=''
curCluster=''
curClusterMax=0.0

mode=1

if len(sys.argv)==2:
	if sys.argv[1]=='-l':
		mode=2
	elif sys.argv[1]=='-w':
		mode=1
	elif sys.argv[1]=='-wl':
		mode=3

for line in sys.stdin:
	line=line.strip()
	if not line:
		break

	IDC=line.split('\t',5)
	tmpCluster=line
	tmpMax=float(IDC[mode])

	if curID=='':
		curID=IDC[0]
		if tmpMax>curClusterMax:
			curCluster=tmpCluster
			curClusterMax=tmpMax
	elif curID==IDC[0]:
		if tmpMax>curClusterMax:
			curCluster=tmpCluster
			curClusterMax=tmpMax
	else:
		sys.stdout.write('%s\n'%curCluster)
		curID=IDC[0]
		curClusterMax=0
		curCluster=tmpCluster

sys.stdout.write('%s\n'%curCluster)
