#!/usr/bin/env python

import math
import sys
import time
import re

if __name__=='__main__':

	curID=''
	cli=''
	num=0
	for line in sys.stdin:
		line=line.strip()
		if not line:continue
		IDC=line.split(';',1)
		if len(IDC)!=2:continue

		if curID=='':
			curID=IDC[0]
			cli=IDC[1].strip()
			num=len(cli.split(';'))
		elif curID==IDC[0]:
			tmp=IDC[1].strip()
			if(len(tmp.split(';'))>num):
				cli=IDC[1].strip()
				num=len(cli.split(';'))
		else:
			sys.stdout.write('%s;\t%s\n'%(curID,cli))
			curID=IDC[0]
			cli=IDC[1].strip()
			num=len(cli.split(';'))
	sys.stdout.write('%s;\t%s\n'%(curID,cli))
