#!/usr/bin/env python
import sys

if __name__=='__main__':
	for line in sys.stdin:
		if not line:continue
		tks=line[:-1].split()
		if len(tks)!=4:continue
		sys.stdout.write('%s\t%s\t%s\n'%(tks[0],tks[2],tks[3]))
