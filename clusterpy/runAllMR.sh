#!/bin/bash

if [ $# == 1 ]
then
	Mode=$1
elif [ $# == 0 ]
then
	Mode=All
else
	echo "Usage: CMD [All|Step]"
fi

Date=`date '+%Y%m%d'`

#directory setup...
#inDir=/user/xce/sg/firendfinder/cluster/userinfo/qinghuausermatrix.txt/*
#inDir=/user/sg/cluster/usermatrix/usermatrix_data/*
inDir=/user/yeyin.zhang/Cluster/usermatrix/usermatrix_data/part-r-00000
#inDir=/user/sg/cluster/usermatrix/usermatrix_encript/
#inDir=/user/sg/cluster/cluster_data/t
outPrefix=/user/yeyin.zhang/Cluster/cluster_data
cliqueSave=$outPrefix/clique$Date
resultSave=$outPrefix/resultSave$Date

#Hadoop fs operation
mkdirfs='hadoop fs -mkdir '

#runner
cliqueCMD='./runSimpleCliqueMR.sh '
clusterCMDIter='./runClusterMRIter.sh '
clusterCMDBatch='./runClusterMRCPP.sh '

rm -rf clique.log cluster.loop.log cluster.log


echo "$mkdirfs $cliqueSave"
echo "$mkdirfs $resultSave"
$mkdirfs $cliqueSave
$mkdirfs $resultSave

#run clique...
echo "$cliqueCMD $inDir $cliqueSave >clique.log"
$cliqueCMD $inDir $cliqueSave >clique.log

if [ $Mode == "Step" ]
then
	echo "$clusterCMDIter $cliqueSave $outPrefix"
	$clusterCMDIter $cliqueSave $outPrefix #run cluster iteratively...
elif [ $Mode == "All" ]
then
	echo "$clusterCMDBatch $Mode \"-input $cliqueSave\" $resultSave >cluster.log"
	$clusterCMDBatch $Mode "-input $cliqueSave" $resultSave >cluster.log #run cluster all in once...
else
	echo "error: run mode error"
	exit
fi
