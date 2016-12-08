#!/usr/bin/env python

from clique import *
from cluster import *
from param import *

import graph as nx

import math
import sys
import time


def outPut(Clusters, schoolnum):
	for n in Clusters:
		c_lst=n[1]
		desc=""
		for i in c_lst:
			desc+='%s;'%i
		sys.stdout.write('%s\t%s\n'%(schoolnum,desc))

if __name__=='__main__':

	default_opts={
		'-t':(4.0,'float','clusterThresh','stop threshhold for hierarchical clustering'),
		'-a':(150.0,'float','alterThresh','find cliques in alternative Graph proceeds alterThresh'),
		'-n':('COMM','str','normType','using the normType to calculate norms in clustering'),
		'-m':('','str','MatrixFile','input matrix data file path'),
		'-u':('','str','UserFile','input id<-->username file path')
		}

	opts=Param(sys.argv[1:],default_opts)

	_clusters=Cluster(None,opts['clusterThresh'])

	curID=''
	for line in sys.stdin:
		line=line.strip()
		if not line:
			continue
		IDC=line.split('\t',6)

		if curID=='':
			curID=IDC[0]
			subj=IDC[1]
			curCluster=IDC[5][:-1].split(';')
			_clusters.append((set([subj]),set(curCluster)|set([subj])))
		elif curID==IDC[0]:
			subj=IDC[1]
			curCluster=IDC[5][:-1].split(';')
			_clusters.append((set([subj]),set(curCluster)|set([subj])))
		else:
			_clusters.cluster_hierarchy()
			_clustersElim=Cluster(_clusters,1,norm_t='MAX')
			_clustersElim.cluster_hierarchy()
			outPut(_clustersElim,curID)
			_clusters=Cluster(None,opts['clusterThresh'])
			curID=IDC[0]
			subj=IDC[1]
			curCluster=IDC[5][:-1].split(';')
			_clusters.append((set([subj]),set(curCluster)|set([subj])))

	_clusters.cluster_hierarchy()
	_clustersElim=Cluster(_clusters,1,norm_t='MAX')
	_clustersElim.cluster_hierarchy()
	outPut(_clustersElim,curID)
	_clusters=Cluster(None,opts['clusterThresh'])
