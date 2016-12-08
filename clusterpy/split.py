#!/usr/bin/python

import sys

def generateLongCountToken(id):
	return "LongValueSum:" + id + "\t" + "1"

def initOutFile(splitNum):
	outdict={}
	for i in xrange(splitNum):
		outdict[i]=open("part-%d"%i,'w')
	return outdict

def dropOutFile(fileDict):
	for f in fileDict:
		fileDict[f].close()

def main(argv):
	if len(argv)!=2:
		sys.stdout.write("parameter : N(num of splits)\n")
		sys.exit()
	spNum=int(argv[1])
	outfileDict=initOutFile(spNum)

	line = sys.stdin.readline();
	try:
		while line:
			line = line[:-1];
			fields = line.split("-");
			if len(fields)>1:
				pn=int(fields[0])%spNum
				outfileDict[pn].write("%s\n"%line)
			#print generateLongCountToken(fields[0]);
			line = sys.stdin.readline();
		dropOutFile(outfileDict)
	except "end of file":
		return None

if __name__ == "__main__":
	main(sys.argv)
