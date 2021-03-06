Hadoop_Streaming=$HADOOP_HOME/mapred/contrib/streaming/hadoop-0.21.0-streaming.jar

if [ ! $# -eq 2 ]
then
	echo "Usage: runCollectMR.sh inPut outPut"
	exit
fi
inPuts=$1
outDir=$2
hadoop fs -rmr $outDir

hadoop jar $Hadoop_Streaming \
-D mapred.compress.map.output=true \
-D mapred.reduce.tasks=40 \
-D mapred.task.timeout=0 \
$inPuts \
-output $outDir \
-mapper "python sgCollectMapper.py" \
-reducer "python sgCollectReducer.py" \
-file sgCollectMapper.py \
-file sgCollectReducer.py \
-file graph.py \
-file clique.py \
-file cluster.py \
-file param.py
