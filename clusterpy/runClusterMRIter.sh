#!/bin/bash
if [ ! $# == 2 ]
then
	echo Usage: CMD inputPath outPrefix
	exit
fi

#directory setup...
cliqueDir=$1
outPrefix=$2
resultSave=$outPrefix/resultSave22
in=$cliqueDir
out=$outPrefix/cluster_0

#Hadoop fs operation
mkdirfs='hadoop fs -mkdir '
rmdirfs='hadoop fs -rmr '

#algorithm runner
clusterCMD='./runClusterMRCPP.sh Step '
collectCMD='./runCollect.sh '
collectMRCMD='./runCollectMR.sh '

i=0
iterMax=100
inputs=""

echo "$mkdirfs $resultSave"
echo "$mkdirfs $out"
$mkdirfs $resultSave
$mkdirfs $out

#run cluster iteratively...
while [ $i -lt $iterMax ]
do
	echo "$i/$iterMax..."
	echo "$clusterCMD \"-input $in\" $out >>cluster.loop.log 2>&1"
	$clusterCMD "-input $in" $out >>cluster.loop.log 2>&1

	result=`hadoop fs -ls $out | awk 'BEGIN{sum=0}{sum+=$5}END{print sum}' `

	j=`expr $i + 1`
	in=$outPrefix/cluster_$i
	out=$outPrefix/cluster_$j
	$mkdirfs $out
	((i++))

	if [[ $result -eq 0 || $j -eq $iterMax ]]
	then
		break
	fi

	inputs="-input $in $inputs"
done

echo "$collectCMD \"$inputs\" $out >>cluster.loop.log 2>&1"
$collectCMD "$inputs" $out >>cluster.loop.log 2>&1

echo "$collectMRCMD \"-input $in -input $out\" $resultSave >>cluster.loop.log 2>&1"
$collectMRCMD "-input $in -input $out" $resultSave >>cluster.loop.log 2>&1
