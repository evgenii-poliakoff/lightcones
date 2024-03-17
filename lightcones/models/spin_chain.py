from lightcones import fock

class spin_chain:
    def __init__(self, length, max_num_flips):
    
        local_bounds = [1]*length
        space = fock.space(statistics = 'Bose', num_modes = length, \
            max_total_occupation = max_num_flips, max_local_occupations = local_bounds)
        self.space = space
        
        self.dimension = space.dimension
        self.zero_op = space.zero_op
        self.eye = space.eye
        
        self.length = length
        self.max_num_flips = max_num_flips
        
        s_m = space.annihilate
        s_p = space.create
        self.s_m = s_m
        self.s_p = s_p
        
        s_x = [space.sigma_x(i) for i in range(length)]
        s_y = [space.sigma_y(i) for i in range(length)]
        s_z = [space.sigma_z(i) for i in range(length)]
        self.s_x = s_x
        self.s_y = s_y
        self.s_z = s_z
        
        self.outer = space.outer