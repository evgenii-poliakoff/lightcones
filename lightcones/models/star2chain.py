import numpy as np
from lightcones import linalg as la

def to_chain(w, J n = None):
    if n is None:
        n = len(w)
    alpha, beta = la.lancz(w, J)
    e = alpha
    h = np.sqrt(beta)
    coupling = h[0]
    h = h[1:]
    return coupling, e, h

def to_star(coupling, e, h):
    H = la.tridiag(e, h)
    H_dense = H.todense()
    w, modes = la.find_eigs_ascending(H_dense)
    J = modes[0,:]**2 * coupling**2
    return w, J 
