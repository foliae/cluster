#!/usr/bin/env python

from clique import *
from cluster import *
from param import *

import graph as nx

import math
import sys
import time

def addToCluster(code,data,Cliques,opts):
	nodes=data[0][:-1].split(';')
	cliqmems=data[-1][:-1].split(';')
	if len(cliqmems)>opts['clusterThresh']:
		Cliques.append((set(nodes[:]),set(nodes[:])|set(cliqmems[:])))
		return 1
	else:
		Cliques.insert(0,(set(nodes[:]),set(nodes[:])|set(cliqmems[:])))
		return 0

def calClusters(Cliques,opts,sep_index):
	clusters=Cluster(Cliques[sep_index:],opts['clusterThresh'])
	print 'sep index: %d/%d'%(sep_index,len(Cliques))
	print "num of centers,",len(clusters)," sep index=",sep_index
	start=time.time()
	clusters.cluster_hierarchy_step()
	#clusters.cluster_hierarchy()
	print "elapsed time=%f"%(time.time()-start)
	if sep_index>0:
		clusters.extend(Cliques[0:sep_index])
	return clusters

def outPutClusters(Clusters, schoolnum):
	print "output ...",len(Clusters)
	for n in Clusters:
		d_lst=n[0]
		c_lst=n[1]
		d_desc=""
		c_desc=""
		for i in d_lst:
			d_desc+='%s;'%i
		for i in c_lst:
			c_desc+='%s;'%i
		sys.stdout.write('%s\t%s\t%s\n'%(schoolnum,d_desc,c_desc))



default_opts={
		'-t':(4.0,'float','clusterThresh','stop threshhold for hierarchical clustering')
		}


if __name__=='__main__':

	opts=Param(sys.argv[1:],default_opts)

	sep_index=0#short cut for clustering
	curID=''
	Cliques=[]
	for line in sys.stdin:
		line=line.strip()
		if not line:
			continue
		IDC=line.split('\t')

		if len(IDC)!=3:
			continue

		if curID=='':
			curID=IDC[0]
			if 0==addToCluster(curID,IDC[1:],Cliques,opts):
				sep_index+=1
		elif curID==IDC[0]:
			if 0==addToCluster(curID,IDC[1:],Cliques,opts):
				sep_index+=1
		else:
			cls=calClusters(Cliques,opts,sep_index)
			outPutClusters(cls,curID)
			Cliques=[]
			curID=IDC[0]
			sep_index=0
			if 0==addToCluster(curID,IDC[1:],Cliques,opts):
				sep_index+=1

	cls=calClusters(Cliques,opts,sep_index)
	outPutClusters(cls,curID)
