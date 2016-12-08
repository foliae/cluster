#/usr/bin/bash

Input=$1
Output=$2

python sg.py $Input

awk '{printf("%s\t%d\n",$1,NR)}' result.labels >idcode
awk '{print $2}' result.labels >labels
python showresult.py >$Output
