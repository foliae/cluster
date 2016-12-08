#/usr/bin/bash

echo $@
if [ $# -eq 1 ]
then
	Input1=$1.userid2friend
	Namelist=$1
elif [ $# -eq 2 ]
then
	Input1=$1
	Namelist=$2
else
	echo 'Usage: ./runclique.sh inputDir';
	exit 1;
fi

T=2
OutputClique=$Input1.result.clique
OutputCluster=$Input1.result.cluster_t$T

echo "python sg.py -m $Input1 -u $Namelist -t 2"
python sg.py -m $Input1 -u $Namelist -t $T

echo "cat clique.info|python showcliqueresult.py $Namelist>$OutputClique"
cat clique.info|python showcliqueresult.py $Namelist>$OutputClique

echo "cat re|python showcliqueresult.py $Namelist>$OutputCluster"
cat re|python showcliqueresult.py $Namelist>$OutputCluster
