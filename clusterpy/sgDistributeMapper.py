import sys
import re

for line in sys.stdin:
	if not line:continue
	line=line.strip()
	tks=line.split()
	if len(tks)!=3:continue
	pairs=tks[2][:-1].split(';')
	if len(pairs)<4:continue
	for p in pairs:
		if not p:continue
		pair=p.split(',')
		sys.stdout.write("%s\t%s;\t%s\n"%(tks[0],pair[0],tks[2]))

