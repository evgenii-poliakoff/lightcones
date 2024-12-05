__all__ = [
    'mv', 
    'lancz',
    'tridiag', 
    'dyad', 
    'as_column_vector', 
    'make_hermitean', 
    'find_largest_eigs', 
    'find_smallest_eigs', 
    'find_eigs_ascending', 
    'find_eigs_descending', 
    'kron'
]

import math
import numpy as np
import scipy.sparse
from scipy.sparse import spdiags
from scipy.linalg import eigh
from typing import List
from typing import Any
from ._fastmul import fastmul
from . import _dlancz

def eye(m):
    return scipy.sparse.eye(m).tocsc()

# compute
# vout = cin * m @ vin + cout * vout
# using the fortran optimized code
# (on intel compiler it is faster then numpy)
def mv(m, vin, vout, cin=1, cout=0):
    fastmul(m.data, m.indices, m.indptr, cin, vin, cout, vout)

# lanczos algorithm
def lancz(w, J, n = None):
    if n is None:
        n = len(w)
    a, b, ierr =  _dlancz.dlancz(n, w, J)
    if ierr != 0:
        raise RuntimeError("dlancz ierr not zero: " + str(ierr))   
    return a, b

# make tridiagonal matrix 
# e: diagonal
# h: upper and lower diagonal
def tridiag(e, h):
    data = [np.concatenate((h, np.array([0]))), np.array(e), np.concatenate((np.array([0]), h))]
    diags = np.array([-1, 0, 1])

    n = len(e)
    return spdiags(data, diags, n, n).tocsc()

# make column vector |ket>
# from the array ket
def as_column_vector(ket):
    shape = ket.shape
    if (len(shape) == 1):
        return ket[:, None]
    if (len(shape) == 2 and shape[1] == 1):
        return ket
    raise RuntimeError("shape of input array is incompatible with the column vector")

# make dyad |ket><bra|
def dyad(ket, bra):
    ket = as_column_vector(ket)
    bra = as_column_vector(bra)
    return np.kron(ket, bra.T.conj())

def projection_to(ket):
    ket = as_column_vector(ket)
    return dyad(ket, ket)

# take Hermitean part of the square matrix m
def make_hermitean(m):
    m += m.T.conj()
    m /= 2

# find k largest eigenvalues of matrix m
# sorted in the descending order
def find_largest_eigs(m, k = None):
    n = len(m)
    if k is None:
        k = n
    k = min(k, n)
    e, v = eigh(m, subset_by_index = [n - k, n - 1])
    e = np.flip(e)
    v = np.flip(v, axis = 1)
    return (e, v)

# find k smallest eigenvalues of matrix m
# sorted in the ascending order
def find_smallest_eigs(m, k = None):
    n = len(m)
    if k is None:
        k = n
    k = min(k, n)
    e, v = eigh(m, subset_by_index = [0, k - 1])
    return (e, v)

# find all eigenvalues of matrix m
# sorted in the ascending order
def find_eigs_ascending(m):
    e, v = eigh(m)
    return (e, v)

# find all eigenvalues of matrix m
# sorted in the descending order
def find_eigs_descending(m):
    e, v = eigh(m)
    e = np.flip(e)
    v = np.flip(v, axis = 1)
    return (e, v)

def is_list_of_any(a):
    return isinstance(a, list)

def is_list_list_of_any(a):
    return all(isinstance(sublist, list) for sublist in a)

# check whether a is a csc_matrix type
def is_sparse_matrix(a):
    return isinstance(a, scipy.sparse.csc_matrix)

# check whether a is a vector type
def is_vector(a):
    return isinstance(a, np.ndarray) and len(a.shape) == 1

def kron_sparse_sparse(a, b):
    return scipy.sparse.kron(a, b, format = 'csc')

def kron_list_sparse(a, b):
    kr = []
    n = len(a)
    for i in range(n):
        kr.append(kron(a[i], b))
        
    return kr

def kron_sparse_list(a, b):
    kr = []
    n = len(b)
    for i in range(n):
        kr.append(kron(a, b[i]))
        
    return kr

def kron_list_list(a, b):
    kr = []
    n = len(a)
    for i in range(n):
        kr.append(kron(a[i], b))
    
    return kr    

def kron_list2_list2(a, b): 
    n1 = len(a)
    m1 = len(a[0])
    n2 = len(b)
    m2 = len(b[0])
    
    kr = []
    for i in range(n1*n2):
        kr.append([])
    
    for i1 in range(n1):
        for j1 in range(m1):
            for i2 in range(n2):
                for j2 in range(m2):
                    kr[i1 * n2 + i2].append(kron(a[i1][j1], b[i2][j2]))
    
    return kr

# kron of sparse matrices a and b
# if either a or b are lists of sparse matrices
# then do elementwise kron

def kron(a, b):
    if is_sparse_matrix(a) and is_sparse_matrix(b):
        return kron_sparse_sparse(a, b)
    
    if is_list_list_of_any(a) and is_list_list_of_any(b):
        return kron_list2_list2(a, b)
    
    if is_list_of_any(a) and is_sparse_matrix(b):
        return kron_list_sparse(a, b)
    
    if is_list_of_any(a) and is_list_of_any(b):
        return kron_list_list(a, b)
    
    if is_sparse_matrix(a) and is_list_of_any(b):
        return kron_sparse_list(a, b)
    
    raise Exception('Unsupported types for kron')


def mul_sparse_vector(a, b):
    vout = np.zeros(len(b), dtype = complex)
    mv(a, b, vout)
    return vout

def mul_sparse_sparse(a, b):
    return a @ b

def mul_list_list_vector(a, b):
    n = len(a)
    m = len(a[0])
    o = []
    for i in range(n):
        row = []
        for j in range(m):
            row.append(mul(a[i][j], b))
        o.append(row)
    return o

def mul_listlist_listlist(a, b):
    n1 = len(a)
    m1 = len(a[0])
    n2 = len(b)
    m2 = len(b[0])
    
    ml = []
    for i in range(n1*n2):
        ml.append([])
    
    for i1 in range(n1):
        for j1 in range(m1):
            for i2 in range(n2):
                for j2 in range(m2):
                    ml[i1 * n2 + i2].append(mul(a[i1][j1], b[i2][j2]))
    
    return ml

# compute a @ b
# if a and b are matrices then matrix multiplication
# if a is matrix and b is vector then matrix-vector multiplication
# if either a or b are lists then elementwise multiplication
def mul(a, b):
    if is_sparse_matrix(a) and is_vector(b):
        return mul_sparse_vector(a, b)
    
    if is_sparse_matrix(a) and is_sparse_matrix(b):
        return mul_sparse_sparse(a, b)
    
    if is_list_list_of_any(a) and is_vector(b):
        return mul_list_list_vector(a, b)
    
    if is_list_list_of_any(a) and is_list_list_of_any(b):
        return mul_listlist_listlist(a, b)
            
    raise Exception('Unsupported type of a for mul')

def dot_vector_vector(a, b):
    return np.vdot(a, b)

def dot_vector_list_list(a, b):
    n = len(b)
    m = len(b[0])
    o = []
    for i in range(n):
        row = []
        for j in range(m):
            row.append(dot(a, b[i][j]))
        o.append(row)
    return o

# inner product of vectors
# if either a or b are lists of vectors
# then elementwise dot product

def dot(a, b):
    if is_vector(a) and is_vector(b):
        return dot_vector_vector(a, b)
    
    if is_vector(a) and is_list_list_of_any(b):
        return dot_vector_list_list(a, b)
            
    raise Exception('Unsupported type of a for dot')

# Lanczos recursion method
# psi0 is assumed to be normalized:
# np.vdot(psi0, psi0) == 1
# H is some matrix which can be muptiplied via @
# returns: n x n tridiagonal matrix
# representation of H
def lancz_recursion(psi0, H, n):
    
    a = np.zeros(n)
    b = np.zeros(n - 1)
    
    psiH = H @ psi0
    a[0] = np.vdot(psiH, psi0)
    psi1 = psiH - a[0] * psi0
    b[1 - 1] = math.sqrt(np.vdot(psi1, psi1))
    psi1 = psi1 / b[1 - 1]
    psiH = H @ psi1
    a[1] = np.vdot(psiH, psi1)
    
    for k in range(2, n):
        psi2 = psiH - a[k - 1] * psi1 - b[k - 1 - 1] * psi0
        b[k - 1] = math.sqrt(np.vdot(psi2, psi2))
        psi2 = psi2 / b[k - 1]
        psiH = H @ psi2
        a[k] = np.vdot(psiH, psi2)
        psi2, psi1, psi0 = psi0, psi2, psi1
    
    return tridiag(a, b)

    
    
    