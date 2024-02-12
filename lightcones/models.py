import numpy as np
import scipy
from scipy.sparse import spdiags
from scipy.linalg import eigh
from scipy import sparse

import math
from numpy import linalg as LA
import scipy.sparse.linalg as sl

from scipy.sparse import coo_matrix

import random

from lightcones.linalg import *
from lightcones import fock

class spin_boson:
    def __init__(self, num_modes, max_num_quanta):
    
        hs_atom = fock.space(statistics = 'Bose', num_modes = 1, max_total_occupation = 1)
        m = num_modes
        n = max_num_quanta
        fs_chain = fock.space(statistics = 'Bose', num_modes = m, max_total_occupation = n) 
        hs_joint = fock.space_kron(hs_atom, fs_chain)
        b_hat = hs_joint.annihilate
        b_hat_dag = hs_joint.create
        sigma_m = b_hat[0]
        sigma_p = b_hat_dag[0]
        sigma = [hs_joint.sigmax(0), hs_joint.sigmay(0), hs_joint.sigmaz(0)]
        a_hat = b_hat[1:]
        a_hat_dag = b_hat_dag[1:]
    
        self.space = hs_joint
        
        self.s_m = sigma_m
        self.s_p = sigma_p
        self.s = sigma
        
        self.s_x = sigma[0]
        self.s_y = sigma[1]
        self.s_z = sigma[2]

        self.a = a_hat
        self.a_dag = a_hat_dag
        
        self.eye = hs_joint.eye
        
        self.num_modes = num_modes
        self.max_num_quanta = max_num_quanta
        
        self.dimension = hs_joint.dimension

        self.zero_op = hs_joint.emptyH
    
class fermion_2_fermion_leads:
    def __init__(self, num_impurity_modes, num_reservoir_modes, max_num_quanta):
        
        import secondquant as sq
        
        self.max_num_quanta = max_num_quanta
        self.num_imp_modes = num_impurity_modes
        self.num_modes = num_reservoir_modes
        
        total_num_modes = num_impurity_modes + 2 * num_reservoir_modes
        
        self.num_tot_modes = total_num_modes
        
        joint = sq.fock_space(num_modes = total_num_modes, max_total_occupation = max_num_quanta, statistics = 'Fermi')
        
        self.d = joint.annihilate[: num_impurity_modes] # impurity modes
        self.d_dag = joint.create[: num_impurity_modes]
        
        self.l = joint.annihilate[num_impurity_modes : num_impurity_modes + num_reservoir_modes] # reservoir modes
        self.l_dag = joint.create[num_impurity_modes : num_impurity_modes + num_reservoir_modes]
        
        self.r = joint.annihilate[num_impurity_modes + num_reservoir_modes :] # reservoir modes
        self.r_dag = joint.create[num_impurity_modes + num_reservoir_modes :]
        
        self.space = joint
        self.dimension = joint.dimension
            
