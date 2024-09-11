from lightcones import fock

# class which computes sparce matrices for spin (two-state) chain 
class spin_chain:
    # length: length of spin chain
    # max_num_flips: keep only states which differ from |00000 ...0> only by no more than
    #  max_num_flips 1's
    def __init__(self, length, max_num_flips):
    
        # at each site, the Hilbert space is truncated at the level of 1 quantum 
        # i.e. only |0> and |1> are retained
        local_bounds = [1]*length
        # create fock space for "length" sites. Keep |0> and |1> at each site. No more than max_num_flips of |1>
        # in the retained basis elements
        space = fock.space(statistics = 'Bose', num_modes = length, \
            max_total_occupation = max_num_flips, max_local_occupations = local_bounds)
        self.space = space
        
        # dimension (number of basis vectors)
        # in a truncated hilbert space
        self.dimension = space.dimension
        self.zero_op = space.zero_op
        self.eye = space.eye
        
        self.length = length
        self.max_num_flips = max_num_flips
        
        # list of sigma_minus Pauli matrices for each site
        s_m = space.annihilate
        # list of sigma_plus Pauli matrices for each site
        s_p = space.create
        self.s_m = s_m
        self.s_p = s_p
        
        # x, y, z Pauli matrices for each site
        s_x = [space.sigma_x(i) for i in range(length)]
        s_y = [space.sigma_y(i) for i in range(length)]
        s_z = [space.sigma_z(i) for i in range(length)]
        self.s_x = s_x
        self.s_y = s_y
        self.s_z = s_z
        
        # ???
        self.outer = space.outer