#!/usr/bin/env python

import math
import sys
from graph import *

class Cluster(list):

	def __init__(self,data,Thresh, stop_k=0, norm_t='COMM',merge_t='Fast'):
		self.T=Thresh
		self.K=stop_k
		self.clusters={}
		self.initNorms()
		self.norm=self.Norms[norm_t]
		self.initPairFinder()
		self.initCenters(data)

		self.findMergePair=self.PairFinder[merge_t]

	def initNorms(self):
		self.Norms={
				'COMM':self.normComm,
				'MAX':self.normMax,
			   }

	def initPairFinder(self):
		self.PairFinder={
				'Fast':self.findMergePairFast,
				'Accu':self.findMergePairAccu,
			   }

	def initCenters(self, data):
		if isinstance(data,dict):
			#print 'dict data'
			n_lst=data.keys()
			for n in n_lst:
				self.append((set([n]),data[n]|set([n])))
		if isinstance(data, list):
			#print 'list data'
			self.extend(data)

	def cluster_hierarchy(self):
		if self.K==0 and self.T==0.0:
			return
		while len(self)>0:
			(sim,index1,index2)=self.findMergePair()
			#print "clustering:...",sim,index1,index2
			if sim<self.T or len(self)<self.K:
				break
			self.updateClusters(index1,index2)
			
	def cluster_hierarchy_step(self):
		if self.K==0 and self.T==0.0:
			return
		if len(self)>0:
			(sim,index1,index2)=self.findMergePair()
			#print "clustering:...",sim,index1,index2
			if sim<self.T or len(self)<self.K:
				return
			self.updateClusters(index1,index2)

	def findMergePairAccu(self):
		#print 'Merge accu...'
		sim=0.0
		index1=-1
		index2=-1
		for i in xrange(len(self)):
			for j in xrange(i+1,len(self)):
				dt=self.norm(i,j)
				if dt>sim:
					sim=dt
					index1=i
					index2=j
		return (sim,index1,index2)

	def findMergePairFast(self):
		#print 'Merge fast...'
		sim=0.0
		index1=-1
		index2=-1
		for i in xrange(len(self)):
			for j in xrange(i+1,len(self)):
				dt=self.norm(i,j)
				if dt>self.T:
					return (dt,i,j)
				if dt>sim:
					sim=dt
					index1=i
					index2=j
		return (sim,index1,index2)

	def updateClusters(self, index1, index2):
		(A,dA)=self[index1]
		(B,dB)=self[index2]
		C=A|B
		dC=dA&dB|A|B
		self.pop(index1)
		self.pop(index2-1)
		self.append((C,dC))


	def normComm(self, i, j):
		if len(self[i][1])==0 or len(self[j][1])==0:
			return 0.0
		d=float(len(self[i][1] & self[j][1]))
		#m=max(d/len(Node1[1]),d/len(Node2[1]))
		#x=m*max(len(Node1[1]),len(Node2[1]))
		return d
		#return math.exp(d)
		#return float(len(Node1[1] & Node2[1]))/float(len(Node1[1] | Node2[1])-len(Node1[1] & Node2[1]))
	
	def normMax(self, i, j):
		if len(self[i][1])==0 or len(self[j][1])==0:
			return 0.0
		d=float(len(self[i][1] & self[j][1]))
		m=max(d/len(self[i][1]),d/len(self[j][1]))
		return float(m)

