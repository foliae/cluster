#!/usr/bin/env python

from clique import *
from cluster import *
from param import *

import graph as nx

import math
import sys
import time

class SG:

	def __init__(self,filename,userfilename):
		self.loadUserDict(userfilename)
		self.parseMatrixFile(filename)
	
	def loadUserDict(self,userfilename):
		try:
			user_file=open(userfilename, 'r')
		except:
			sys.exit('File open error:%s'%userfilename)
		
		self.userdict={}
		for line in user_file:
			idnameline=line.strip()
			idname=idnameline.split('\t',2)
			userid=""
			username=""
			if len(idname)==2:
				userid=idname[0]
				username=idname[1]
			elif len(idname)==1:
				userid=idname[0]
				username=idname[0]
			else:
				continue
			#print userid, username

			if self.userdict.has_key(userid):
				#print 'warning: already has ', userid, 'in userdict' 
				continue
			else:
				self.userdict[userid]=username
		#print self.userdict.keys()
			
	def parseMatrixFile(self,filename):
		try:
			matrix_file=open(filename, 'r')
		except:
			sys.exit('file open error:%s'%filename)
		
		self.social_matrix={}
		line_num=0
		for line in matrix_file:
			line_num+=1
			subject = line.strip()
			vertex = subject.split('\t',4)

			if len(vertex)!=4:
				#print 'matrix file format error in file:',filename,'in line:',line_num
				continue;

			subject_id = vertex[0]
			subject_distance_sum = float(vertex[1])
			subject_connections_num = float(vertex[2])
			subject_connections = vertex[3]
			
			connections=subject_connections.split(';')
			
			subject_connections={}

			for connect in connections:
				#if n==10:
					#break
				if not connect:
					continue
				else:
					#n+=1
					subject_connect=connect.split(',')
					connect_id=subject_connect[0]
					connect_distance=float(subject_connect[1])
				
					if connect_id==subject_id:
						#print "warning: id and connect id duplicate:",subject_id,connect_id
						continue
					if subject_connections.has_key(connect_id):
						#print 'warning: already has ',connect_id,' in subject_connections'
						continue
					else:
						subject_connections[connect_id]=connect_distance
						#print connect_distance
			
			if self.social_matrix.has_key(subject_id):
				#print 'warning: already has ', subject_id, ' in social_matrix'
				continue
			else:
				self.social_matrix[subject_id]=subject_connections
		
		matrix_file.close()

	def social_graph(self,secondary_graph=False):
		visit={}
		self.edge_single={}
		if secondary_graph==True:
			self.G_double=nx.Graph()
		self.G_single=nx.Graph()
		#self.traverse_BFS(self.G, start,visit)
		keys=self.social_matrix.keys()
		for key in keys:
			self.traverse_single(self.G_single, key)
			if secondary_graph==True:
				self.traverse_double(self.G_double, key)

		if secondary_graph==True:
			return self.G_single,self.G_double
		else:
			return self.G_single

	def traverse_BFS(self,graph, node, visit):
		subject_conn_dict={}
		if self.social_matrix.has_key(node):
			subject_conn_dict=self.social_matrix[node]
			
		for child in subject_conn_dict.keys():
			if self.userdict.has_key(child) or len(self.userdict)==0:
				clicks_num=subject_conn_dict[child]
				visit[node]=True
				if clicks_num > 0:
					#w = math.log(subject_conn_dict[child])
					w = subject_conn_dict[child]
					if visit.has_key(child):
						if(graph.has_edge(node,child)):
							graph[node][child]['weight']+=w
						else:
							graph.add_edge(node, child, weight=w)
					else:
						if(graph.has_edge(node,child)):
							graph[node][child]['weight']+=w
						else:
							graph.add_edge(node, child, weight=w)
						self.traverse_BFS(graph, child, visit)

	def traverse_single(self,graph, node):
		subject_conn_dict={}
		if self.social_matrix.has_key(node):
			subject_conn_dict=self.social_matrix[node]
			
		for child in subject_conn_dict.keys():
			if self.userdict.has_key(child) or len(self.userdict)==0:
				clicks_num=subject_conn_dict[child]
				if clicks_num > 0.0:
					#w = math.log(subject_conn_dict[child])
					w = subject_conn_dict[child]
					if graph.has_edge(node,child):
						graph[node][child]['weight']+=w
					else:
						graph.add_edge(node, child, weight=w)

	def traverse_double(self,graph, node):
		subject_conn_dict={}
		if self.social_matrix.has_key(node):
			subject_conn_dict=self.social_matrix[node]
			
		for child in subject_conn_dict.keys():
			if self.userdict.has_key(child) or len(self.userdict)==0:
				clicks_num=subject_conn_dict[child]
				if clicks_num > 0.0:
					#w = math.log(subject_conn_dict[child])
					w = subject_conn_dict[child]
					if self.edge_single.has_key(child+node):
						graph.add_edge(node,child,weight=w+self.edge_single[child+node])
					else:
						self.edge_single[node+child]=w



def outPut(Cliques, schoolnum,G=None):
	for n in Cliques.cliques.keys():
		c_lst=Cliques.cliques[n]
		edge_weights=0.0
		desc=""
		w=0.0
		for i in c_lst:
			if G is not None:
				w=G[n][i]['weight']
				edge_weights+=w
			desc+='%s;'%i

		attr='%f\t%d\t%f\t'%(edge_weights,len(c_lst),edge_weights/len(c_lst))
		sys.stdout.write('%d\t%s\t%s%s\n'%(schoolnum,n,attr,desc))

if __name__=='__main__':

	default_opts={
		'-t':(4.0,'float','clusterThresh','stop threshhold for hierarchical clustering'),
		'-a':(150.0,'float','alterThresh','find cliques in alternative Graph proceeds alterThresh'),
		'-m':('','str','MatrixFile','input matrix data file path'),
		'-u':('','str','UserFile','input id<-->username file path')
		}

	opts=Param(sys.argv[1:],default_opts)
	num=0
	for line in sys.stdin:
		if not line:
			continue
		tks=line[:-1].split()
		if len(tks)!=2 and len(tks)!=4:
			continue
		opts['MatrixFile']=tks[0]
		opts['UserFile']=tks[1]
		sg1=SG(opts['MatrixFile'],opts['UserFile'])
		G1_single=sg1.social_graph()
		cf=CliqueFinder()
		cf.find_cliques_alternative(G1_single)
		num+=1
		outPut(cf,num)
