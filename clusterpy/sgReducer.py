#!/usr/bin/env python

from clique import *
from cluster import *
from param import *

import graph as nx

import math
import sys
import time

def add(code,data,Users,G):
	addToUser(code,data,Users)
	addToGraph(code,data,G)

def addToUser(code,data,Users):
	Users.append(data[0])

def addToGraph(code,data,G):
	node=data[0]
	nbrs=data[-1].split(',')
	for child in nbrs:
		if not child:
			continue
		if child==node or G.has_edge(node,child):
			continue
		else:
			G.add_edge(node,child,weight=0.0)

def calClusters(Users,G,opts):
	subG=G.subgraph(Users)
	cliqueFinder=CliqueFinder()
	cliqueFinder.find_cliques_alternative(subG)
	clusters=Cluster(cliqueFinder.cliques,opts['clusterThresh'])
	clusters.cluster_hierarchy()
	clustersElim=Cluster(clusters,1,norm_t='MAX')
	clustersElim.cluster_hierarchy()
	return clustersElim

def outPut(Clusters, schoolnum):
	for n in Clusters:
		c_lst=n[1]
		desc=""
		for i in c_lst:
			desc+='%s;'%i
		sys.stdout.write('%s\t%s\n'%(schoolnum,desc))


default_opts={
		'-t':(4.0,'float','clusterThresh','stop threshhold for hierarchical clustering')
		}


if __name__=='__main__':

	opts=Param(sys.argv[1:],default_opts)

	curID=''
	Users=[]
	sg=Graph()
	for line in sys.stdin:
		line=line.strip()
		if not line:
			continue
		IDC=line.split('\t')

		if len(IDC)!=2 and len(IDC)!=3:
			continue

		if curID=='':
			curID=IDC[0]
			add(curID,IDC[1:],Users,sg)
		elif curID==IDC[0]:
			add(curID,IDC[1:],Users,sg)
		else:
			print curID
			cls=calClusters(Users,sg,opts)
			outPut(cls,curID)
			Users=[]
			sg=Graph()
			curID=IDC[0]
			add(curID,IDC[1:],Users,sg)

	print curID
	cls=calClusters(Users,sg,opts)
	outPut(cls,curID)
