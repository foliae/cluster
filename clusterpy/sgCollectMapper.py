import sys
import re

for line in sys.stdin:
	if not line:continue
	line=line.strip()
	tks=line.split()
	if len(tks)==3 or len(tks)==4:
		sys.stdout.write('%s\n'%line)
