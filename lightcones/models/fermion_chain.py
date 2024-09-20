from lightcones import fock

# class which computes sparce matrices for the model of fermionic chain
 

class fermion_chain:
    # length: length of chain
    # max_total_excitations: truncate the Fock space by keeping no more than
    # max_total_excitations excitations above the vacuum 
    def __init__(self, length, max_total_excitations):
    
        # at each site, the Hilbert space is truncated at the level of 1 quantum 
        # i.e. only |0> and |1> are retained
        local_bounds = [1]*length
        # create fock space with 'Fermi' statistics for "length" sites. Keep |0> and |1> at each site. No more than max_total_excitations of |1>
        # in the retained basis elements
        space = fock.space(statistics = 'Fermi', num_modes = length, \
            max_total_occupation = max_total_excitations)
        self.space = space
        
        # dimension (number of basis vectors)
        # in a truncated Fock space
        self.dimension = space.dimension
        # zero operator
        self.zero_op = space.zero_op
        # identity matrix
        self.eye = space.eye
        
        self.length = length
        self.max_total_excitations = max_total_excitations
        
        # list of annihilation operators 
        # a[0] ... a[length-1]
        a = space.annihilate
        # list of annihilation operators
        # a_dag[0] ... a_dag[length-1]
        a_dag = space.create
        self.a = a
        self.a_dag = a_dag
            
        # ???
        self.outer = space.outer