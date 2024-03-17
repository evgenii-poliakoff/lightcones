from lightcones import fock

class fermion_chain:
    def __init__(self, length, max_total_excitations):
    
        local_bounds = [1]*length
        space = fock.space(statistics = 'Fermi', num_modes = length, \
            max_total_occupation = max_total_excitations)
        self.space = space
        
        self.dimension = space.dimension
        self.zero_op = space.zero_op
        self.eye = space.eye
        
        self.length = length
        self.max_total_excitations = max_total_excitations
        
        a = space.annihilate
        a_dag = space.create
        self.a = a
        self.a_dag = a_dag
            
        self.outer = space.outer