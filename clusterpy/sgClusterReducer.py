#!/usr/bin/env python

from clique import *
from cluster import *
from param import *

import graph as nx

import math
import sys
import time
import re

def addToCluster(data,Cliques,supports,opts):
	p=re.compile(',|;')
	cen=p.split(data[-2][:-1])
	l=p.split(data[-1][:-1])
	ids=[l[i] for i in range(len(l)) if i %2 == 0]
	weis=[l[i] for i in range(len(l)) if i %2 != 0]
	for i in xrange(len(ids)):
		if supports.has_key(ids[i]):
			if int(weis[i])>supports[ids[i]]:
				supports[ids[i]]=int(weis[i])
		else:
			supports[ids[i]]=int(weis[i])
	if len(ids)>=opts['clusterThresh']:
		Cliques.append((set(cen),set(ids)))
		return 1
	else:
		Cliques.insert(0,(set(cen),set(ids)))
		return 0

def calClusters(Cliques,sID,opts,sep_index,supports):
	if opts['runMode']=='All':
		calClustersBatch(Cliques,sID,opts['clusterThresh'],opts['mergeMode'],opts['distance'],sep_index,supports)
	elif opts['runMode']=='Step':
		calClustersStep(Cliques,sID,opts['clusterThresh'],opts['mergeMode'],opts['distance'],sep_index,supports)

def calClustersBatch(Cliques,sID,thresh,Merge,distance,sep_index,supports):
	clusters=Cluster(Cliques[sep_index:],thresh,norm_t=distance, merge_t=Merge)
	#print 'sep index: %d/%d'%(sep_index,len(Cliques))
	#print "num of centers,",len(clusters)," sep index=",sep_index
	#start=time.time()
	#clusters.cluster_hierarchy_step()
	clusters.cluster_hierarchy()
	#print "elapsed time=%f"%(time.time()-start)
	if sep_index>0:
		clusters.extend(Cliques[0:sep_index])
	outPutClustersDone(clusters,sID,supports)

def calClustersStep(Cliques,sID,thresh, Merge, distance, sep_index,supports):
	preLen=len(Cliques)
	clusters=Cluster(Cliques[sep_index:],thresh,norm_t=distance, merge_t=Merge)
	#print 'sep index: %d/%d'%(sep_index,len(Cliques))
	#print "num of centers,",len(clusters)," sep index=",sep_index
	#start=time.time()
	clusters.cluster_hierarchy_step()
	#print "elapsed time=%f"%(time.time()-start)
	if sep_index>0:
		clusters.extend(Cliques[0:sep_index])
	proLen=len(clusters)
	if preLen>proLen:
		outPutClusters(clusters,sID,supports)
	else:
		outPutClustersDone(clusters,sID,supports)

def outPutClusters(Clusters, schoolnum,supports):
	#print "output ...",len(Clusters)
	for n in Clusters:
		if n is None:continue
		cdesc=""
		ddesc=""
		numM=0.0
		for i in n[0]:
			cdesc+='%s;'%i
		for i in n[1]:
			ddesc+='%s,%d;'%(i,supports[i])
			numM+=supports[i]
		sys.stdout.write('%s\t%f\t%s\t%s\n'%(schoolnum,numM/len(n[1]),cdesc,ddesc))

def outPutClustersDone(Clusters, schoolnum,supports):
	#print "output ...",len(Clusters)
	numC=0
	for n in Clusters:
		if n is None:continue
		ddesc=""
		numM=0.0
		if len(n[1])<5:continue
		ne=n[0]|n[1]
		for i in ne:
			ddesc+='%s,%d;'%(i,supports[i])
			numM+=supports[i]
		sys.stdout.write('%s-%d\t%f\t%s\n'%(schoolnum,numC,numM/len(ne),ddesc))
		numC+=1
	supports.clear()
	Clusters=[]



default_opts={
		'-r':('All','str','runMode','run clustering in iterative or batch mode: All/Step'),
		'-m':('Accu','str','mergeMode','Merge method of clustering: Accu/Fast'),
		'-n':('COMM','str','distance','OPTIM/COMM'),
		'-t':(4.0,'float','clusterThresh','stop threshhold for hierarchical clustering')
		}


if __name__=='__main__':

	opts=Param(sys.argv[1:],default_opts)

	sep_index=0#short cut for clustering
	curID=''
	Cliques=[]
	supports={}
	for line in sys.stdin:
		line=line.strip()
		if not line:
			continue
		IDC=line.split('\t')

		if len(IDC)!=3:
			continue

		if curID=='':
			curID=IDC[0]
			if 0==addToCluster(IDC[1:],Cliques,supports,opts):
				sep_index+=1
		elif curID==IDC[0]:
			if 0==addToCluster(IDC[1:],Cliques,supports,opts):
				sep_index+=1
		else:
			cls=calClusters(Cliques,curID,opts,sep_index,supports)
			Cliques=[]
			curID=IDC[0]
			supports={}
			sep_index=0
			if 0==addToCluster(IDC[1:],Cliques,supports,opts):
				sep_index+=1

	cls=calClusters(Cliques,curID,opts,sep_index,supports)
