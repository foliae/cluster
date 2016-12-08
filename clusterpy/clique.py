"""
=======
Cliques
=======

Find and manipulate cliques of graphs.
"""
from graph import *

class CliqueFinder:
	def __init__(self,stop_iter=None,stop_t=None,info=None):
		self.stop_t=stop_t
		self.stop_iter=stop_iter
		self.cliques={}
		self.info=info

	def find_cliques_alternative(self, G1):
		for n,nbrs in G1.adjacency_iter():
			clique,size_clique=self.find_maxlen_cliques_with_node(G1,n,nbrs)
			if size_clique!=0:
				self.cliques[n]=clique


	def write(self, write_to_file, G):
		clique_info=open(write_to_file,'w')

		for n in self.cliques.keys():
			c_lst=self.cliques[n]
			edge_weights=0.0
			desc=""
			w=0.0
			for i in c_lst:
				w=G[n][i]['weight']
				edge_weights+=w
				desc+='%s;'%i

			attr='%f\t%d\t%f\t'%(edge_weights,len(c_lst),edge_weights/len(c_lst))
			clique_info.write('%s\t%s%s\n'%(n,attr,desc))

		clique_info.close()


	def find_cliques(self, G):
		# Cache nbrs and find first pivot (highest degree)
		maxconn=-1
		nnbrs={}
		pivotnbrs=set() # handle empty graph
		for n,nbrs in G.adjacency_iter():
			conn = len(nbrs)
			if conn > maxconn:
				nnbrs[n] = pivotnbrs = set(nbrs)
				maxconn = conn
			else:
				nnbrs[n] = set(nbrs)

		# Initial setup
		cand=set(nnbrs)
		smallcand = cand - pivotnbrs
		done=set()
		stack=[]
		clique_so_far=[]
		# Start main loop
		cliqueNum=0
		while smallcand or stack:
			try:
				# Any nodes left to check?
				n=smallcand.pop()
			except KeyError:
				# back out clique_so_far
				cand,done,smallcand = stack.pop()
				clique_so_far.pop()
				continue
			# Add next node to clique

			clique_so_far.append(n)
			cand.remove(n)
			done.add(n)
			nn=nnbrs[n]
			new_cand = cand & nn
			new_done = done & nn
			# check if we have more to search
			if not new_cand: 
				if not new_done:
					# Found a clique!
					#self.outClique(clique_so_far[:],cliqueNum)
					yield clique_so_far[:]
					cliqueNum+=1
				clique_so_far.pop()
				continue
			# Shortcut--only one node left!
			if not new_done and len(new_cand)==1:
				yield clique_so_far+list(new_cand)
				cliqueNum+=1
				clique_so_far.pop()
				continue
			# find pivot node (max connected in cand)
			# look in done nodes first
			numb_cand=len(new_cand)
			maxconndone=-1
			for n in new_done:
				cn = new_cand & nnbrs[n]
				conn=len(cn)
				if conn > maxconndone:
					pivotdonenbrs=cn
					maxconndone=conn
					if maxconndone==numb_cand:
						break
			# Shortcut--this part of tree already searched
			if maxconndone == numb_cand:  
				clique_so_far.pop()
				continue
			# still finding pivot node
			# look in cand nodes second
			maxconn=-1
			for n in new_cand:
				cn = new_cand & nnbrs[n]
				conn=len(cn)
				if conn > maxconn:
					pivotnbrs=cn
					maxconn=conn
					if maxconn == numb_cand-1:
						break
			# pivot node is max connected in cand from done or cand
			if maxconndone > maxconn:
				pivotnbrs = pivotdonenbrs
			# save search status for later backout
			stack.append( (cand, done, smallcand) )
			cand=new_cand
			done=new_done
			smallcand = cand - pivotnbrs

		return




	def find_maxlen_cliques_with_node(self, G, node, node_list=None):
		if node_list is not None:
			g=G.subgraph(node_list)
		else:
			g=G.subgraph(G[node].keys())
		clique=set()
		size=0
		# Cache nbrs and find first pivot (highest degree)
		maxconn=-1
		nnbrs={}
		pivotnbrs=set() # handle empty graph
		for n,nbrs in g.adjacency_iter():
			conn = len(nbrs)
			if conn > maxconn:
				nnbrs[n] = pivotnbrs = set(nbrs)
				maxconn = conn
			else:
				nnbrs[n] = set(nbrs)

		# Initial setup
		cand=set(nnbrs)
		smallcand = cand - pivotnbrs
		done=set()
		stack=[]
		clique_so_far=[]
		num_iter=0
		while smallcand or stack:
			num_iter+=1
			print "num_iter",num_iter
			if self.stop_iter is not None and self.stop_iter<num_iter:
				return clique,size
			if self.stop_t is not None and self.stop_t<len(clique):
				return clique.size
			try:
				# Any nodes left to check?
				n=smallcand.pop()
			except KeyError:
				# back out clique_so_far
				cand,done,smallcand = stack.pop()
				clique_so_far.pop()
				continue
			# Add next node to clique

			clique_so_far.append(n)
			cand.remove(n)
			done.add(n)
			nn=nnbrs[n]
			new_cand = cand & nn
			new_done = done & nn
			# check if we have more to search
			if not new_cand: 
				if not new_done:
					# Found a clique!
					if len(clique_so_far[:])>size:
						clique=set(clique_so_far[:])
						size=len(clique)
				clique_so_far.pop()
				continue
			# Shortcut--only one node left!
			if not new_done and len(new_cand)==1:
				if len(clique_so_far + list(new_cand))>size:
					clique=set(clique_so_far+list(new_cand))
					size=len(clique)
				clique_so_far.pop()
				continue
			# find pivot node (max connected in cand)
			# look in done nodes first
			numb_cand=len(new_cand)
			maxconndone=-1
			for n in new_done:
				cn = new_cand & nnbrs[n]
				conn=len(cn)
				if conn > maxconndone:
					pivotdonenbrs=cn
					maxconndone=conn
					if maxconndone==numb_cand:
						break
			# Shortcut--this part of tree already searched
			if maxconndone == numb_cand:  
				clique_so_far.pop()
				continue
			# still finding pivot node
			# look in cand nodes second
			maxconn=-1
			for n in new_cand:
				cn = new_cand & nnbrs[n]
				conn=len(cn)
				if conn > maxconn:
					pivotnbrs=cn
					maxconn=conn
					if maxconn == numb_cand-1:
						break
			# pivot node is max connected in cand from done or cand
			if maxconndone > maxconn:
				pivotnbrs = pivotdonenbrs
			# save search status for later backout
			stack.append( (cand, done, smallcand) )
			cand=new_cand
			done=new_done
			smallcand = cand - pivotnbrs

		return clique,size

	def find_mostfriend_cliques_with_node(self, G,G_friend, node, node_list=None):
		if node_list is not None:
			g=G.subgraph(node_list)
		else:
			g=G.subgraph(G[node].keys())
		clique=set()
		size=0

		if G_friend.has_node(node):
			friends=G_friend[node].keys()
			friendset=set(friends)
		else:
			friends=G_friend.nodes()
			friendset=set(friends)

		# Cache nbrs and find first pivot (highest degree)
		maxconn=-1
		nnbrs={}
		pivotnbrs=set() # handle empty graph
		for n,nbrs in g.adjacency_iter():
			conn = len(nbrs)
			if conn > maxconn:
				nnbrs[n] = pivotnbrs = set(nbrs)
				maxconn = conn
			else:
				nnbrs[n] = set(nbrs)

		# Initial setup
		cand=set(nnbrs)
		smallcand = cand - pivotnbrs
		done=set()
		stack=[]
		clique_so_far=[]
		# Start main loop
		while smallcand or stack:
			try:
				# Any nodes left to check?
				n=smallcand.pop()
			except KeyError:
				# back out clique_so_far
				cand,done,smallcand = stack.pop()
				clique_so_far.pop()
				continue
			# Add next node to clique

			clique_so_far.append(n)
			cand.remove(n)
			done.add(n)
			nn=nnbrs[n]
			new_cand = cand & nn
			new_done = done & nn
			# check if we have more to search
			if not new_cand: 
				if not new_done:
					# Found a clique!
					nodeset=set(clique_so_far[:])
					if len(friendset & nodeset)>size:
					#if len(clique_so_far[:])>size:
						clique=set(clique_so_far[:])
						size=len(clique)
				clique_so_far.pop()
				continue
			# Shortcut--only one node left!
			if not new_done and len(new_cand)==1:
				nodeset=set(clique_so_far+list(new_cand))
				if len(friendset & nodeset)>size:
				#if len(clique_so_far + list(new_cand))>size:
					clique=set(clique_so_far+list(new_cand))
					size=len(clique)
				clique_so_far.pop()
				continue
			# find pivot node (max connected in cand)
			# look in done nodes first
			numb_cand=len(new_cand)
			maxconndone=-1
			for n in new_done:
				cn = new_cand & nnbrs[n]
				conn=len(cn)
				if conn > maxconndone:
					pivotdonenbrs=cn
					maxconndone=conn
					if maxconndone==numb_cand:
						break
			# Shortcut--this part of tree already searched
			if maxconndone == numb_cand:  
				clique_so_far.pop()
				continue
			# still finding pivot node
			# look in cand nodes second
			maxconn=-1
			for n in new_cand:
				cn = new_cand & nnbrs[n]
				conn=len(cn)
				if conn > maxconn:
					pivotnbrs=cn
					maxconn=conn
					if maxconn == numb_cand-1:
						break
			# pivot node is max connected in cand from done or cand
			if maxconndone > maxconn:
				pivotnbrs = pivotdonenbrs
			# save search status for later backout
			stack.append( (cand, done, smallcand) )
			cand=new_cand
			done=new_done
			smallcand = cand - pivotnbrs

		return clique,size

	def find_maxweight_cliques_with_node(self, G, node,node_list=None):
		if node_list is not None:
			g=G.subgraph(node_list)
		else:
			g=G.subgraph(G[node].keys())
		clique=set()
		maxweight=0.0

		# Cache nbrs and find first pivot (highest degree)
		maxconn=-1
		nnbrs={}
		pivotnbrs=set() # handle empty graph
		for n,nbrs in g.adjacency_iter():
			conn = len(nbrs)
			if conn > maxconn:
				nnbrs[n] = pivotnbrs = set(nbrs)
				maxconn = conn
			else:
				nnbrs[n] = set(nbrs)

		# Initial setup
		cand=set(nnbrs)
		smallcand = cand - pivotnbrs
		done=set()
		stack=[]
		clique_so_far=[]
		# Start main loop
		while smallcand or stack:
			try:
				# Any nodes left to check?
				n=smallcand.pop()
			except KeyError:
				# back out clique_so_far
				cand,done,smallcand = stack.pop()
				clique_so_far.pop()
				continue
			# Add next node to clique

			clique_so_far.append(n)
			cand.remove(n)
			done.add(n)
			nn=nnbrs[n]
			new_cand = cand & nn
			new_done = done & nn
			# check if we have more to search
			if not new_cand: 
				if not new_done:
					# Found a clique!
					weight=sum(G[node][nbr]['weight'] for nbr in clique_so_far[:] if nbr!=node)
					if weight>maxweight:
					#if len(clique_so_far[:])>size:
						clique=set(clique_so_far[:])
						maxweight=weight
				clique_so_far.pop()
				continue
			# Shortcut--only one node left!
			if not new_done and len(new_cand)==1:
				weight=sum(G[node][nbr]['weight'] for nbr in clique_so_far+list(new_cand) if nbr!=node)
				if weight>maxweight:
				#if len(clique_so_far + list(new_cand))>size:
					clique=set(clique_so_far+list(new_cand))
					maxweight=weight
				clique_so_far.pop()
				continue
			# find pivot node (max connected in cand)
			# look in done nodes first
			numb_cand=len(new_cand)
			maxconndone=-1
			for n in new_done:
				cn = new_cand & nnbrs[n]
				conn=len(cn)
				if conn > maxconndone:
					pivotdonenbrs=cn
					maxconndone=conn
					if maxconndone==numb_cand:
						break
			# Shortcut--this part of tree already searched
			if maxconndone == numb_cand:  
				clique_so_far.pop()
				continue
			# still finding pivot node
			# look in cand nodes second
			maxconn=-1
			for n in new_cand:
				cn = new_cand & nnbrs[n]
				conn=len(cn)
				if conn > maxconn:
					pivotnbrs=cn
					maxconn=conn
					if maxconn == numb_cand-1:
						break
			# pivot node is max connected in cand from done or cand
			if maxconndone > maxconn:
				pivotnbrs = pivotdonenbrs
			# save search status for later backout
			stack.append( (cand, done, smallcand) )
			cand=new_cand
			done=new_done
			smallcand = cand - pivotnbrs

		return clique,maxweight

