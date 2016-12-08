Hadoop_Streaming=$HADOOP_HOME/mapred/contrib/streaming/hadoop-0.21.0-streaming.jar

if [ ! $# -eq 2 ]
then
	echo "Usage: runCliqueMR.sh inPut outPut"
	exit
fi

inDir=$1
outDir=$2
hadoop fs -rmr $outDir

hadoop jar $Hadoop_Streaming \
-D mapred.compress.map.output=true \
-D mapred.reduce.tasks=40 \
-D mapred.task.timeout=0 \
-input $inDir \
-output $outDir \
-mapper "python sgSimpleCliqueMapper.py" \
-reducer "python sgSimpleCliqueReducer.py" \
-file sgSimpleCliqueMapper.py \
-file sgSimpleCliqueReducer.py \
-file graph.py \
-file param.py 
