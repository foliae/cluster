#!/usr/bin/env python

import scipy
from scipy.sparse.linalg.eigen.arpack import eigen_symmetric
from scipy.cluster.vq import kmeans, kmeans2,whiten
import time

def sc(Array, num_clusters, sigma=0):
	"""
	SC Spectral clustering using a sparse similarity matrix (t-nearest-neighbor).
	Input  : A              : N-by-N sparse distance matrix, where
                                 N is the number of data
                sigma          : sigma value used in computing similarity,
                                 if 0, apply self-tunning technique
                num_clusters   : number of clusters
    
       Output : cluster_labels : N-by-1 vector containing cluster labels
                evd_time       : running time for eigendecomposition
                kmeans_time    : running time for k-means
                total_time     : total running time

	Author : Yeyin Zhang (zhangyeyin@gmail.com)
    
	Convert the sparse distance matrix to a sparse similarity matrix,
	where S = exp^(-(A^2 / 2*sigma^2)).
	Note: This step can be ignored if A is sparse similarity matrix.
	"""

	print 'Coverting distance matrix to similarity matrix...'
	start=time.time()

	n=Array.shape[0]
	powerA=Array*Array
	#powerA=(-1)*Array*Array

	if sigma==0: # selftuning spectral clustering
	#Find the count of nonzero for each column
		print 'Selftuning spectral clustering'
		col_ones=scipy.logical_and(Array, scipy.ones(Array.shape))
		col_count=scipy.sum(col_ones,axis=0)
		col_sum=scipy.sum(Array,axis=0)

		col_count=scipy.logical_not(scipy.logical_and(col_count,scipy.ones(col_count.shape)))+col_count
		col_sum=scipy.logical_not(scipy.logical_and(col_sum,scipy.ones(col_sum.shape)))+col_sum

		col_mean=col_sum / col_count
		norm=col_mean.reshape((n,1))*col_mean

		normA=powerA/norm/2.0
		#print 'normA',normA
	else:
		print 'Fixed-sigma spectral clustering'
		normA=powerA/sigma/sigma/2

	ones_normA=scipy.logical_and(scipy.ones(normA.shape),normA)
	expA=scipy.exp(normA)*ones_normA
	#print 'normA:',normA
	#print 'expA:',expA

	print 'elapsed time:',time.time()-start,'s'

	#Do laplacian, L=D^(-1/2)*S*D^(-1/2)
	print 'Doing laplacian...'

	D=scipy.sum(expA,axis=1)+scipy.exp(-10)
	D=scipy.sqrt(1/D)
	D=scipy.diag(D)
	DexpA=scipy.dot(D,expA)
	L=scipy.dot(DexpA,D)

	print 'elapsed time:',time.time()-start,'s'
    
	print 'Performing eigen decompostion...'
	val,V=eigen_symmetric(L,k=num_clusters)
	print 'eigenvectors:',V
	print 'eigenvalues:',val

	print 'elapsed time:',time.time()-start,'s'

	print 'Performing kmeans...'
	# normalize each row to be of unit length
	sq_sum=scipy.sqrt(scipy.sum(V*V,1))+scipy.exp(-20)
	sq_sum=sq_sum.reshape((n,1))
	sq_sum_t=sq_sum
    
	for i in range(1,num_clusters):
		sq_sum_t=scipy.concatenate((sq_sum_t,sq_sum),axis=1)

	U=V / sq_sum_t
    
	print 'U for kmeans',U
	cluster_centroid,cluster_labels=kmeans2(U,num_clusters,minit='points')
	print 'cluster labels:',cluster_labels
	#cluster_centroid_km,cluster_labels_km=kmeans2(whiten(Array+Array.T),num_clusters,minit='points')
	scipy.savetxt('testdata.txt.labels',cluster_labels,fmt='%d')
	#scipy.savetxt('testdata.txt.labels_km',cluster_labels_km,fmt='%d')

	print 'elapsed time:',time.time()-start,'s'
	print 'Finished'
	return (cluster_labels,cluster_centroid,U)

if __name__=="__main__":
	a=scipy.loadtxt("testdata.txt")
	L,C,U=sc(a,2)
