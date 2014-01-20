# @author: Marion


import numpy as np
import scipy.linalg as spla
import scipy.sparse as spsp


def normalizeKernel(K):
    K_min = np.float(np.min(K))
    K_max = np.float(np.max(K))  
    #K_norm = (K - K_min)/(np.float(K_max-K_min))
    K_norm = K/K_max
    
    if np.isnan(np.sum(K_norm)):
        print K_max 
        print K_min
        print K_norm
        print K
        print '======================'
        exit()
    return K_norm


def regLapKernel(A, sigma=1):
    ''' Regularized Laplacian Kernel 
        
    :param A:  adjacency matrix
    :param sigma: (hyper)parameter(s)
    '''

    I = np.identity(A.shape[0])
    d = A.sum(axis=0)
    
    # normalized Laplacian
    d = np.sqrt(1./d)    
    D = np.diag(d)
    L = I - np.dot( np.dot(D,A),D )

    K = np.linalg.inv( I+(sigma**2)*L )
    return K


def psInvLapKernel(A):
    ''' Pseudo inverse of the normalized Laplacian.

    :param A:  adjacency matrix
    '''

    I = np.identity(A.shape[0])
    d = A.sum(axis=0)
    
    # normalized Laplacian
    d = np.sqrt(1./d)    
    D = np.diag(d)
    L = I - np.dot( np.dot(D,A),D )

    K = np.linalg.pinv(L)
    return K


def diffKernel(A, beta=0.5):
    ''' Diffusion Process Kernel 
        
    K = exp(beta * H), where H = -L = A-D
    
    K = Q exp(beta * Lambda) Q.T
        
    :param A:  adjacency matrix
    :param beta: (hyper)parameter(s)
    '''

    A = np.array(A) # make sure that A is a numpy array!!

    H = A - np.diag(np.sum(A, axis=1))
    w, Q = np.linalg.eigh(H)
    Lambda = np.diag(np.exp(beta*w))
    K = np.dot(np.dot(Q, Lambda), Q.T)

    return K


def VNDKernel(A, alpha=0.5):
    '''  Von Neumann Diffusion Kernel on graph (Zhou et al., 2004)
    (also label spreading kernel)
        
    K = (I - alpha*S)^-1, where S = D^-1/2*A*D^-1/2
        
    :param A:  adjacency matrix
    :param alpha: (hyper)parameter(s)
    '''
        
    I = np.identity(A.shape[0])
    d = A.sum(axis=0)
    d = np.sqrt(1./d)    
    D = np.diag(d)
    S = np.dot( np.dot(D,A),D )

    K = np.linalg.inv( I - alpha*S )
    return K



def rwKernel(A, p=2, a=2):
    '''
    p-step Random Walk Kernel with a>1
       
    K = (aI-L)^p, p>1 and L is the normalized Laplacian 
     
    :param A:  adjacency matrix
    :param p:  step parameter
    :param a:  (hyper)parameter(s)
    '''

    if p < 2:
	raise Exception('Step parameter p needs to be larger than 1.') 	

    if a <= 1:	
	a=1.0001

    I = np.identity(A.shape[0])
    d = A.sum(axis=0)
    
    # normalized Laplacian
    d = np.sqrt(1./d)    
    D = np.diag(d)
    L = I - np.dot( np.dot(D,A),D )

    K = np.linalg.matrix_power( a*I - L, int(p) )	

    return K



def cosKernel(A):
    ''' Cosine Kernel (also Inverse Cosine Kernel)
            
    :param A:  adjacency matrix
            
    NOT IMPLEMENTED IN THIS VERSION
    '''
        
    K = 'not implemented'
    return K 



