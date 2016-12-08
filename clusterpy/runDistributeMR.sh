Hadoop_Streaming=/data/hadoop/hadoop/mapred/contrib/streaming/hadoop-0.21.0-streaming.jar

if [ ! $# -eq 2 ]
then
	echo "Usage: runDistributeMR.sh inPut outPut"
	exit
fi

inDir=$1
outDir=$2
hadoop fs -rmr $outDir

hadoop jar $Hadoop_Streaming \
-D mapred.task.timeout=0 \
-D stream.num.map.output.key.fields=2 \
-D mapred.reduce.tasks=20 \
-input $inDir \
-output $outDir \
-mapper "python sgDistributeMapper.py" \
-reducer "python sgDistributeReducer.py" \
-file sgDistributeMapper.py \
-file sgDistributeReducer.py
#-D mapred.compress.map.output=true \
