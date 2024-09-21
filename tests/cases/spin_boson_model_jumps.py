# test the quantum jumps sampling

# import the required packages
import numpy as np
from lightcones.linalg import mv
import lightcones as lc
from lightcones import models
from lightcones.jumps import make_jump
from lightcones.solvers.schrodinger import solve

class trajectory():
    
    def __init__(self):
    
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
        
        self.ti_arrival = ti_arrival
        
        # causal diamond frame
        cd_dim = 4
        self.cd_dim = cd_dim
        spread_cd, U_cd = lc.causal_diamond_frame(spread_min, ti_arrival, U_min, rho_plus_min, dt, rtol, cd_dim)
        
        # moving frame
        spread_mv, H_mv = lc.moving_frame(spread_cd, ti_arrival, U_cd, dt, cd_dim)
        self.spread_mv = spread_mv
        self.H_mv = H_mv
        
        # Now solve the spin boson model in the moving frame
        num_modes = 15
        max_num_quanta = 5
        m = models.spin_boson(num_modes, max_num_quanta)
        self.m = m

        wq = 1.0
        Hs = wq * m.s_p @ m.s_m
        self.Hs = Hs
        g = 0.05
        V = g * m.s_m
        V_dag = g * m.s_p
        self.V_dag = V_dag

        # Time step
        dt = 0.01
        self.dt = dt

        # Final grid
        t_max = 100
        t = np.arange(0, t_max + dt, dt)
        self.t = t
        n_time = t.size
        self.n_time = n_time

        def f(ti):
            return(0.1*np.cos((ti + 0.5)*self.dt))
        
        self.f = f
        
        psi_0 = np.zeros(m.dimension, dtype = complex)
        psi_0[0] = 1
        self.psi_0 = psi_0

        self.Ht = None
        self.Hint = m.space.zero_op
        self.m_out_prev = 0

        def begin_step(ti, psi):
            m_out, m_in = lc.get_inout_range(self.ti_arrival, ti, self.cd_dim)
            if m_in > 0:
                self.Hint = self.V_dag @ sum(self.spread_mv[m_out : m_in, ti] * self.m.a[m_out : m_in])
                self.Hint = self.Hint + self.Hint.conj().transpose()
            self.Ht = self.Hs + self.m.s_x * self.f(ti) + self.Hint
            Hw = self.m.zero_op
            W = lc.get_H(self.ti_arrival, self.H_mv, ti)
            if not W is None:
                for p in range(m_in - m_out):
                    for q in range(m_in - m_out):
                        Hw += 1j * self.m.a_dag[m_out + q] @ self.m.a[m_out + p] * W[q, p].conj()
            self.Ht = self.Ht + Hw
            
        self.begin_step = begin_step
    
        def apply_h(ti, psi_in, psi_out):
            mv(self.Ht, psi_in, psi_out)

        self.apply_h = apply_h

        # Here we store the average of observables
        self.s_z_av = []

        def eval_o(ti, psi):
            self.s_z_av.append(np.vdot(psi, self.m.s_z @ psi))
            
        self.eval_o = eval_o
    
    def solve(self):
        
        self.s_z_av = []
        
        solve(0, self.n_time-1, self.dt, self.apply_h, self.psi_0, begin_step = self.begin_step, eval_o = self.eval_o)
        
        s_z_av = np.array(self.s_z_av)
        s_z_av_table = np.column_stack((self.t, s_z_av.real))
        
        return s_z_av_table
    
    