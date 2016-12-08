#!/usr/bin/env python
import sys

if len(sys.argv)!=5:
	print "Usage: CMD -l|-w|-wl value result1 result2"
	exit()

mode_str=sys.argv[1]
thresh=sys.argv[2]
result1=sys.argv[3]
result2=sys.argv[4]

mode=2

if mode_str=="-l":
	mode=2
elif mode_str=="-w":
	mode=1
elif mode_str=="-wl":
	mode=3

result={}

result1=open(result1,'r')
result2=open(result2,'r')

for line in result2:
	line=line.strip()
	items=line.split('\t')
	if len(items)!=5:
		continue
	if items[mode]>thresh:
		result[items[0]]=line


for line in result1:
	line=line.strip()
	items=line.split('\t')
	if len(items)!=5:
		continue
	if result.has_key(items[0]):
		continue
	else:
		result[items[0]]=line


for item in result:
	print item
