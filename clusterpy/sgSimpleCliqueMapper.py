#!/usr/bin/env python
import sys

if __name__=='__main__':
	for line in sys.stdin:
		if not line:
			continue
		tks=line[:-1].split()
		if len(tks)!=3:
			continue
		sys.stdout.write('%s\t%s\t%s\n'%(tks[1],tks[0],tks[2]))
