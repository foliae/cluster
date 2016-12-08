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
	preLen=len(Cliques)
	clusters=Cluster(Cliques[sep_index:],opts['clusterThresh'])
	#print 'sep index: %d/%d'%(sep_index,len(Cliques))
	#print "num of centers,",len(clusters)," sep index=",sep_index
	#start=time.time()
	clusters.cluster_hierarchy_step()
	#clusters.cluster_hierarchy()
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
		ddesc=""
		numM=0.0
		for i in n[1]:
			ddesc+='%s,%d;'%(i,supports[i])
			numM+=supports[i]
		sys.stdout.write('%s-%d\t%f\t%s\n'%(schoolnum,numC,numM/len(n[1]),ddesc))
		numC+=1



default_opts={
		'-t':(4.0,'float','clusterThresh','stop threshhold for hierarchical clustering')
		}


if __name__=='__main__':

	opts=Param(sys.argv[1:],default_opts)

	curID=''
	num=0
	for line in sys.stdin:
		line=line.strip()
		if not line:
			continue
		IDC=line.split('\t')

		if len(IDC)==3:
			sys.stdout.write('%s\n'%line)
			continue
		if len(IDC)!=4:
			continue

		if curID=='':
			curID=IDC[0]
			sys.stdout.write('%s-%d\t%s\t%s\n'%(IDC[0],num,IDC[1],IDC[3]))
			num+=1
		elif curID==IDC[0]:
			sys.stdout.write('%s-%d\t%s\t%s\n'%(IDC[0],num,IDC[1],IDC[3]))
			num+=1
		else:
			curID=IDC[0]
			num=0
			sys.stdout.write('%s-%d\t%s\t%s\n'%(IDC[0],num,IDC[1],IDC[3]))
			num+=1
