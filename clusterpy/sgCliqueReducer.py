#!/usr/bin/env python

from clique import *
from cluster import *
from param import *

import graph as nx

import math
import sys
import time

def addToClique(code,data,Users,G):
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

def calCliquesAll(Users,G,opts,schoolnum):
	subG=G.subgraph(Users)
	cliqueFinder=CliqueFinder()
	for cli in cliqueFinder.find_cliques(subG):
		if len(cli)>1:
			outCliqueAll(cli,subG,schoolnum)

def outCliqueAll(clique,G,schoolnum):
	w=len(clique)
	desc=""
	degreeSum=0
	for c in clique:
		degree=len(G[c])
		degreeSum+=degree
		desc+='%s,%d;'%(c,degree)
	support=float(degreeSum)/w
	sys.stdout.write('%s\t%f\t%s\n'%(schoolnum,support,desc))

def calCliques(Users,G,opts,schoolnum):
	subG=G.subgraph(Users)
	#cliqueFinder=CliqueFinder(200,100)
	#cliqueFinder=CliqueFinder(15000)
	cliqueFinder=CliqueFinder()
	for n,nbrs in subG.adjacency_iter():
		clique,size_clique=cliqueFinder.find_maxlen_cliques_with_node(subG,n,nbrs)
		if size_clique!=0:
			outClique(n,set([n])|clique,subG,schoolnum)

def outClique(n,clique,G,schoolnum):
	w=len(clique)
	desc=""
	degreeSum=0
	for c in clique:
		degree=len(G[c])
		degreeSum+=degree
		desc+='%s,%d;'%(c,degree)
	support=float(degreeSum)/w
	sys.stdout.write('%s\t%f\t%s;\t%s\n'%(schoolnum,support,n,desc))

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
			addToClique(curID,IDC[1:],Users,sg)
		elif curID==IDC[0]:
			addToClique(curID,IDC[1:],Users,sg)
		else:
			cls=calCliquesAll(Users,sg,opts,curID)
			Users=[]
			sg=Graph()
			curID=IDC[0]
			addToClique(curID,IDC[1:],Users,sg)

	cls=calCliquesAll(Users,sg,opts,curID)
