import sys

for line in sys.stdin:
	if not line:continue
	line=line.strip()
	sys.stdout.write("%s\n"%line)
