Hadoop_Streaming=/data/hadoop/hadoop/mapred/contrib/streaming/hadoop-0.21.0-streaming.jar

if [ ! $# -eq 3 ]
then
	echo "Usage: runClusterMR.sh [All|Step] inPut outPut"
	exit
fi

Mode=$1
inPuts=$2
outDir=$3
hadoop fs -rmr $outDir

hadoop jar $Hadoop_Streaming \
-D mapred.compress.map.output=true \
-D mapred.reduce.tasks=100 \
-D mapred.task.timeout=0 \
$inPuts \
-output $outDir \
-mapper "python sgClusterMapper.py" \
-reducer "python sgClusterReducer.py -r $Mode" \
-file sgClusterMapper.py \
-file sgClusterReducer.py \
-file graph.py \
-file clique.py \
-file cluster.py \
-file param.py 
