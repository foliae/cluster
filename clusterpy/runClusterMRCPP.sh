Hadoop_Streaming=$HADOOP_HOME/mapred/contrib/streaming/hadoop-0.21.0-streaming.jar

if [ ! $# -eq 3 ]
then
	echo "Usage: runClusterMRCPP.sh [All|Step] inPut outPut"
	exit
fi

Mode=$1
inPuts=$2
outDir=$3
hadoop fs -rmr $outDir

hadoop jar $Hadoop_Streaming \
-D mapred.reduce.tasks=40 \
-D mapred.task.timeout=0 \
$inPuts \
-output $outDir \
-mapper "./sgClusterMapper" \
-reducer "./sgClusterReducerCached $Mode -t 4" \
-file sgClusterMapper \
-file sgClusterReducerCached
