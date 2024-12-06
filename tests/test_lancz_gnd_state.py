import numpy as np
import lightcones.linalg as ll
import lightcones.models as lm

tol = 1e-10

def test_lancz_gnd_state():
    
    f = lm.spinfull_fermions(5)
    
    U = 1
    t = 0.05
    
    H_hopp = sum([sum([- t * (f.a_dag[s][i] @ f.a[s][i - 1] + f.a_dag[s][i - 1] @ f.a[s][i]) for s in range(2)]) for i in range(5)])
    H_S = H_hopp + sum([U * f.n[0][i] @ f.n[1][i] for i in range(5)])
    
    H_S_ = H_S.todense()
    e_expected, v_expected = ll.find_smallest_eigs(H_S_, 1)
    
    psi0 = np.zeros(f.dimension, dtype = complex)
    psi0[0] = 1.0
    psi0 = f.a_dag[0][3] @ f.a_dag[1][3] @ psi0
    e_actual, v_actual = ll.lancz_gnd_state(psi0, H_S, 10)
    
    assert abs(e_expected - e_actual) < tol, \
        f"e does not match"
        
    assert abs(np.vdot(v_expected, v_actual) - 1.0) < tol, \
        f"v does not match"