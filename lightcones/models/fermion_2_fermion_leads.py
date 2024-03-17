from lightcones import fock

class fermion_2_fermion_leads:
    def __init__(self, num_impurity_modes, num_reservoir_modes, max_num_quanta):
             
        self.max_num_quanta = max_num_quanta
        self.num_imp_modes = num_impurity_modes
        self.num_modes = num_reservoir_modes
        
        total_num_modes = num_impurity_modes + 2 * num_reservoir_modes
        
        self.num_tot_modes = total_num_modes
        
        joint = fock.space(statistics = 'Fermi', num_modes = total_num_modes, max_total_occupation = max_num_quanta)
        
        self.d = joint.annihilate[: num_impurity_modes] # impurity modes
        self.d_dag = joint.create[: num_impurity_modes]
        
        self.l = joint.annihilate[num_impurity_modes : num_impurity_modes + num_reservoir_modes] # reservoir modes
        self.l_dag = joint.create[num_impurity_modes : num_impurity_modes + num_reservoir_modes]
        
        self.r = joint.annihilate[num_impurity_modes + num_reservoir_modes :] # reservoir modes
        self.r_dag = joint.create[num_impurity_modes + num_reservoir_modes :]
        
        self.space = joint
        self.dimension = joint.dimension
        
        self.zero_op = joint.zero_op
            
