# test the quantum jumps sampling

# import the required packages
import numpy as np
from lightcones.linalg import mv
import lightcones as lc
from lightcones import models
from lightcones.jumps import make_jump
from lightcones.solvers.schrodinger import solve
import random

class mvf:

    def __init__(self):
        pass

    def compute_s_z_av(self, n_samples, seed = None):
            
        if not seed is None:
            random.seed(seed)
            
        # construct the moving frame:
        
        # chain
        n_sites = 100
        # on-site energies
        es = [1]*n_sites
        # hoppings
        hs = [0.05]*(n_sites-1)

        # time grid
        dt = 0.01
        nt = 10000

        # spread
        spread = lc.spread(es, hs, nt, dt)

        # rho_plus
        rho_plus = lc.rho_plus(spread, dt)

        # minimal forward light cone
        rtol = 10**(-4)
        ti_arrival, spread_min, U_min, rho_plus_min = lc.minimal_forward_frame(spread, rho_plus, dt, rtol)
        
        # causal diamond frame
        cd_dim = 4
        spread_cd, U_cd = lc.causal_diamond_frame(spread_min, ti_arrival, U_min, rho_plus_min, dt, rtol, cd_dim)
        
        # moving frame
        spread_mv, H_mv = lc.moving_frame(spread_cd, ti_arrival, U_cd, dt, cd_dim)
        
        # Now solve the spin boson model in the moving frame
        num_modes = cd_dim
        max_num_quanta = 5
        m = models.spin_boson(num_modes, max_num_quanta)

        wq = 1.0
        Hs = wq * m.s_p @ m.s_m
        g = 0.05
        V = g * m.s_m
        V_dag = g * m.s_p

        # Time step
        dt = 0.01

        # Final grid
        t_max = 100
        t = np.arange(0, t_max + dt, dt)
        n_time = t.size

        def f(ti):
            return(0.1*np.cos((ti + 0.5)*dt))

        psi_0 = np.zeros(m.dimension, dtype = complex)
        psi_0[0] = 1

        self.Ht = None
        self.Hint = m.space.zero_op
        self.m_out_prev = 0

        def to_ring(ti):
            return ti % cd_dim

        def begin_step(ti, psi):
            m_out, m_in = lc.get_inout_range(ti_arrival, ti, cd_dim)
            
            # if the number of decoupled modes is changed: we need to make a jump
            if m_out != self.m_out_prev:
                psi[:] = make_jump(psi, m.space, to_ring(self.m_out_prev) + 1) # + 1 because the first mode is the qubit
                self.m_out_prev = m_out 
            
            if m_in > 0:
                a = m.zero_op
                for p in range(m_in - m_out):
                    a = a + spread_mv[m_out + p, ti] * m.a[to_ring(m_out + p)]
                self.Hint = V_dag @ a
                self.Hint = self.Hint + self.Hint.conj().transpose()
            self.Ht = Hs + m.s_x * f(ti) + self.Hint
            Hw = m.zero_op
            W = lc.get_H(ti_arrival, H_mv, ti)
            if not W is None:
                for p in range(m_in - m_out):
                    for q in range(m_in - m_out):
                        Hw += 1j * m.a_dag[to_ring(m_out + q)] @ m.a[to_ring(m_out + p)] * W[q, p].conj()
            self.Ht = self.Ht + Hw
    
        def apply_h(ti, psi_in, psi_out):
            mv(self.Ht, psi_in, psi_out)

        # Here we store the average of observables
        s_z_av = np.zeros(n_time)

        def eval_o(ti, psi):
            s_z_av[ti] = s_z_av[ti] + np.vdot(psi, m.s_z @ psi)

        for i in range(n_samples):
            self.m_out_prev = 0
            solve(0, n_time-1, dt, apply_h, psi_0, begin_step = begin_step, eval_o = eval_o)
        
        s_z_av_table = np.column_stack((t, s_z_av.real))
        
        return s_z_av_table