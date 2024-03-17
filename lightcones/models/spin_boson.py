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
        sigma = [hs_joint.sigma_x(0), hs_joint.sigma_y(0), hs_joint.sigma_z(0)]
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

        self.zero_op = hs_joint.zero_op