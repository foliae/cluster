Hadoop_Streaming=/data/hadoop/hadoop/mapred/contrib/streaming/hadoop-0.21.0-streaming.jar

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
-D mapred.reduce.tasks=1 \
-D mapred.task.timeout=0 \
-input $inDir \
-output $outDir \
-mapper "python sgCliqueMapper.py" \
-reducer "python sgCliqueReducer.py" \
-file sgCliqueMapper.py \
-file sgCliqueReducer.py \
-file graph.py \
-file clique.py \
-file cluster.py \
-file param.py 
