from lightcones import fock

# class which computes sparce matrices for the model of 2 fermionic leads
 

class fermion_2_fermion_leads:
    # num_impurity_modes: number of modes on which the impurity resides
    # num_reservoir_modes: number of modes for each revervoir (left/right)
    # max_num_quanta: truncate the joint (impurity + leads) Fock space by keeping no more than
    # max_num_quanta excitations above the vacuum 
    def __init__(self, num_impurity_modes, num_reservoir_modes, max_num_quanta):
             
        self.max_num_quanta = max_num_quanta
        self.num_imp_modes = num_impurity_modes
        self.num_modes = num_reservoir_modes
        
        # total number of modes in the system
        total_num_modes = num_impurity_modes + 2 * num_reservoir_modes
        
        self.num_tot_modes = total_num_modes
        
        # joint fermionic Fock space
        joint = fock.space(statistics = 'Fermi', num_modes = total_num_modes, max_total_occupation = max_num_quanta)
        
        # list of annihilation operators for impurity 
        # d[0] ... d[num_impurity_modes-1]
        self.d = joint.annihilate[: num_impurity_modes] # impurity modes
        # list of creation operators for impurity 
        # d_dag[0] ... d_dag[num_impurity_modes-1]
        self.d_dag = joint.create[: num_impurity_modes]
        
        # list of annihilation operators for left reservoir
        # l[0] ... l[num_reservoir_modes-1]
        self.l = joint.annihilate[num_impurity_modes : num_impurity_modes + num_reservoir_modes] # reservoir modes
        # list of creation operators for left reservoir
        # l_dag[0] ... l_dag[num_reservoir_modes-1]
        self.l_dag = joint.create[num_impurity_modes : num_impurity_modes + num_reservoir_modes]
        
        # list of annihilation operators for right reservoir
        # r[0] ... r[num_reservoir_modes-1]
        self.r = joint.annihilate[num_impurity_modes + num_reservoir_modes :] # reservoir modes
        # list of creation operators for right reservoir
        # r_dag[0] ... r_dag[num_reservoir_modes-1]
        self.r_dag = joint.create[num_impurity_modes + num_reservoir_modes :]
        
        # joint Fock space
        self.space = joint
        # dimension (number of basis vectors)
        # in a truncated Fock space
        self.dimension = joint.dimension
        
        # zero operator
        self.zero_op = joint.zero_op
            
