from lightcones import fock


# class which computes sparce matrices for spin-boson model 
class spin_boson:
    # num_modes: number of sites in bosonic chain
    # max_num_quanta: max. total number of quanta to keep in a truncated Hilbert space
    def __init__(self, num_modes, max_num_quanta):
    
        # two-state Hilbert space of spin (atom)
        hs_atom = fock.space(statistics = 'Bose', num_modes = 1, max_total_occupation = 1)
        m = num_modes
        n = max_num_quanta
        # Hilbert space of bosonic chain
        fs_chain = fock.space(statistics = 'Bose', num_modes = m, max_total_occupation = n) 
        # joint space
        hs_joint = fock.space_kron(hs_atom, fs_chain)
        # annihilation operator for the joint system
        b_hat = hs_joint.annihilate
        # creation operators for the joint system
        b_hat_dag = hs_joint.create
        # annihilation operator on site 0
        # has the same matrix elements as sigma_minus Pauli matrix
        # (in the basis of |0> and |1>)
        sigma_m = b_hat[0]
        # creation operator on site 0
        # has the same matrix elements as sigma_plus Pauli matrix
        # (in the basis of |0> and |1>)
        sigma_p = b_hat_dag[0]
        # vector of Pauli matrices (x, y, z)
        sigma = [hs_joint.sigma_x(0), hs_joint.sigma_y(0), hs_joint.sigma_z(0)]
        a_hat = b_hat[1:]
        a_hat_dag = b_hat_dag[1:]
    
        # joint space
        self.space = hs_joint
        
        self.s_m = sigma_m
        self.s_p = sigma_p
        self.s = sigma
        
        self.s_x = sigma[0]
        self.s_y = sigma[1]
        self.s_z = sigma[2]

        self.a = a_hat
        self.a_dag = a_hat_dag
        
        # identity matrix
        self.eye = hs_joint.eye
        
        self.num_modes = num_modes
        self.max_num_quanta = max_num_quanta
        
        # dimension (number of basis vectors)
        # in a truncated hilbert space
        self.dimension = hs_joint.dimension

        # zero operator
        self.zero_op = hs_joint.zero_op