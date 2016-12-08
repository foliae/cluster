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


#directory setup...
#inDir=/user/xce/sg/firendfinder/cluster/userinfo/qinghuausermatrix.txt/*
#inDir=/user/sg/cluster/usermatrix/usermatrix_data/*
inDir=/user/sg/cluster/usermatrix/usermatrix_data/part-r-00000
#inDir=/user/sg/cluster/cluster_data/t
outPrefix=/user/sg/cluster/cluster_data
cliqueSave=$outPrefix/clique0311
resultSave=$outPrefix/resultSave0311

#Hadoop fs operation
mkdirfs='hadoop fs -mkdir '

#runner
cliqueCMD='./runSimpleCliqueMR.sh '
clusterCMDIter='./runClusterMRIter.sh '
clusterCMDBatch='./runClusterMRCPP.sh '


echo "$mkdirfs $cliqueSave"
echo "$mkdirfs $resultSave"
$mkdirfs $cliqueSave
$mkdirfs $resultSave


if [ -f clique.log ]
then
	rm clique.log
fi

if [ -f cluster.loop.log ]
then
	rm cluster.loop.log
fi

if [ -f cluster.log ]
then
	rm cluster.log
fi

#run clique...
echo "$cliqueCMD $inDir $cliqueSave >&clique.log"
#$cliqueCMD $inDir $cliqueSave >&clique.log

if [ $Mode == "Step" ]
then
	echo "$clusterCMDIter $cliqueSave $outPrefix"
	$clusterCMDIter $cliqueSave $outPrefix #run cluster iteratively...
elif [ $Mode == "All" ]
then
	echo "$clusterCMDBatch $Mode "-input $cliqueSave" $resultSave >&cluster.log"
	$clusterCMDBatch $Mode "-input $cliqueSave" $resultSave >&cluster.log #run cluster all in once...
else
	echo "error: run mode error"
	exit
fi
