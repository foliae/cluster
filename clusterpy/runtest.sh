PYTHON=/cygdrive/c/Python26/python.exe

echo $@
if [ ! $# -eq 3 ]
then
	echo "Usage:Python DataFile NameFile value_thresh;"
	exit;
fi
echo $1 $2 $3

DataFile=$1
NameFile=$2
value_thresh=$3

$PYTHON sg.py $DataFile $NameFile -t $value_thresh
