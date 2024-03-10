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
from scipy.sparse import spdiags
from scipy.linalg import eigh
from multipledispatch import dispatch
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

@dispatch(scipy.sparse.csc_matrix, scipy.sparse.csc_matrix)
def kron(a, b):
    return scipy.sparse.kron(a, b, format = 'csc')

@dispatch(List[List[Any]], List[List[Any]])
def kron(a, b):
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
