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

import numpy as np
import scipy.sparse
from scipy.sparse import spdiags
from scipy.linalg import eigh
from typing import List
from typing import Any
from ._fastmul import fastmul
from . import _dlancz

def mv(m, vin, vout, cin=1, cout=0):
    fastmul(m.data, m.indices, m.indptr, cin, vin, cout, vout)

def lancz(w, J, n = None):
    if n is None:
        n = len(w)
    a, b, ierr =  _dlancz.dlancz(n, w, J)
    if ierr != 0:
        raise RuntimeError("dlancz ierr not zero: " + str(ierr))   
    return a, b

def tridiag(e, h):
    data = [np.concatenate((h, np.array([0]))), np.array(e), np.concatenate((np.array([0]), h))]
    diags = np.array([-1, 0, 1])

    n = len(e)
    return spdiags(data, diags, n, n).tocsc()

def dyad(ket, bra):
    return np.kron(ket, bra.T.conj())

def as_column_vector(ket):
    return ket[:, None]

def make_hermitean(m):
    m += m.T.conj()
    m /= 2

def find_largest_eigs(m, k = None):
    n = len(m)
    if k is None:
        k = n
    k = min(k, n)
    e, v = eigh(m, subset_by_index = [n - k, n - 1])
    e = np.flip(e)
    v = np.flip(v, axis = 1)
    return (e, v)

def find_smallest_eigs(m, k = None):
    n = len(m)
    if k is None:
        k = n
    k = min(k, n)
    e, v = eigh(m, subset_by_index = [0, k - 1])
    return (e, v)

def find_eigs_ascending(m):
    e, v = eigh(m)
    return (e, v)

def find_eigs_descending(m):
    e, v = eigh(m)
    e = np.flip(e)
    v = np.flip(v, axis = 1)
    return (e, v)

def is_list_list_of_any(a):
    return all(isinstance(sublist, list) for sublist in a)

def is_sparse_matrix(a):
    return isinstance(a, scipy.sparse.csc_matrix)

def is_vector(a):
    return isinstance(a, np.ndarray) and len(a.shape) == 1

def kron_sparse_sparse(a, b):
    return scipy.sparse.kron(a, b, format = 'csc')

def kron_list_list(a, b): 
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

def kron(a, b):
    if is_sparse_matrix(a) and is_sparse_matrix(b):
        return kron_sparse_sparse(a, b)
    
    if is_list_list_of_any(a) and is_list_list_of_any(b):
        return kron_list_list(a, b)
    
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

def dot(a, b):
    if is_vector(a) and is_vector(b):
        return dot_vector_vector(a, b)
    
    if is_vector(a) and is_list_list_of_any(b):
        return dot_vector_list_list(a, b)
            
    raise Exception('Unsupported type of a for dot')