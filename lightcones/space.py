import numpy as np
import scipy
from scipy.sparse import coo_matrix


class bounding_condition:
    @staticmethod
    def none():
        return lambda state: False
    
    @staticmethod
    def more_than_singly_occupied():
        return lambda state: max(state) > 1
    
    @staticmethod
    def more_than_n_occupied(n):
        return lambda state: max(state) > n
    
    @staticmethod
    def more_than_in_total(n):
        return lambda state: sum(state) > n

class skip_condition:
    @staticmethod
    def none():
        return lambda state: False
    
    @staticmethod
    def odd():
        return lambda state: sum(state) % 2 != 0

class states:
    def __init__(self, num_modes, bounding_condition, skip_condition = skip_condition.none()):
        self.num_modes = num_modes
        self.skip_condition = skip_condition
        self.bounding_condition = bounding_condition
        self.all_states = list(self.state_generator())
        self.enumerated_states = {state: idx for idx, state in enumerate(self.all_states)}
        self.dimension = len(self.all_states)
        
    def state_generator(self):
        current_state = (0,) * self.num_modes
        while True:
            if (not self.skip_condition(current_state)):
                yield current_state
            j = self.num_modes - 1
            current_state = current_state[:j] + (current_state[j]+1,)
            while self.bounding_condition(current_state):
                j -= 1
                if j < 0:
                    return
                current_state = current_state[:j] + (current_state[j]+1, 0) + current_state[j+2:]
            
    def state_at(self, index):
        return self.all_states[index]
    
    def index_of(self, state):
        return self.enumerated_states[state]
            
class bosons:
    def __init__(self, states):
        self.states = states
        
        #
        self.zero = coo_matrix((self.states.dimension , self.states.dimension), dtype = complex).tocsc()      
        
        #
        self.eye = scipy.sparse.eye(self.states.dimension).tocsc()
        
        #
        self.a = []
        for k in range(self.states.num_modes):
            row = np.zeros(self.states.dimension)
            col = np.arange(self.states.dimension, dtype=int)
            data = np.zeros(self.states.dimension)
            for i in range(self.states.dimension):
                in_state = self.states.all_states[i]
                if not in_state[k] == 0:
                    out_state = in_state[:k] + (in_state[k]-1,) + in_state[k+1:]
                    ind = self.states.index_of(out_state)
                    row[i] = ind
                    data[i]=(in_state[k])**0.5
            a_k = coo_matrix((data, (row, col)), shape=(self.states.dimension , self.states.dimension), dtype = complex)
            a_k.eliminate_zeros()
            self.a.append(a_k.tocsc())
                
        #
        self.a_dag=[]
        for k in range(self.states.num_modes):
            row = np.zeros(self.states.dimension)
            col = np.arange(self.states.dimension, dtype=int)
            data = np.zeros(self.states.dimension)
            for i in range(self.states.dimension):
                in_state = self.states.all_states[i]
                out_state = in_state[:k] + (in_state[k]+1,) + in_state[k+1:]
                if not self.states.bounding_condition(out_state):
                    ind = self.states.index_of(out_state)
                    row[i] = ind
                    data[i]=(out_state[k])**0.5
            a_k_dag = coo_matrix((data, (row, col)), shape=(self.states.dimension , self.states.dimension), dtype = complex)
            a_k_dag.eliminate_zeros()
            self.a_dag.append(a_k_dag.tocsc())
            
    def vac(self):
        state = np.zeros(self.states.dimension, dtype = complex)
        state[0] = 1.0
        return state
            
class fermions:
    def __init__(self, states):
        self.states = states
        
        more_than_singly = bounding_condition.more_than_singly_occupied()
        
        #
        self.zero = coo_matrix((self.states.dimension , self.states.dimension), dtype = complex).tocsc()      
        
        #
        self.eye = scipy.sparse.eye(self.states.dimension).tocsc()
        
        # parity operator
        data = np.zeros(self.states.dimension)
        for i in range(self.states.dimension):
            p = sum(self.states.state_at(i))
            data[i] = (-1)**p
        self.parity = scipy.sparse.diags(data).tocsc()
        
        #
        self.a = []
        for k in range(self.states.num_modes):
            row = np.zeros(self.states.dimension)
            col = np.arange(self.states.dimension, dtype=int)
            data = np.zeros(self.states.dimension)
            for i in range(self.states.dimension):
                in_state = self.states.all_states[i]
                if not in_state[k] == 0:
                    out_state = in_state[:k] + (in_state[k]-1,) + in_state[k+1:]
                    ind = self.states.index_of(out_state)
                    row[i] = ind
                    p = sum(in_state[:k])
                    data[i]=(-1)**p * (in_state[k])**0.5
            a_k = coo_matrix((data, (row, col)), shape=(self.states.dimension , self.states.dimension), dtype = complex)
            a_k.eliminate_zeros()
            self.a.append(a_k.tocsc())
                
        #
        self.a_dag=[]
        for k in range(self.states.num_modes):
            row = np.zeros(self.states.dimension)
            col = np.arange(self.states.dimension, dtype=int)
            data = np.zeros(self.states.dimension)
            for i in range(self.states.dimension):
                in_state = self.states.all_states[i]
                if more_than_singly(in_state):
                    raise ValueError("Using more than singly occupied states to construct fermionic operators")
                out_state = in_state[:k] + (in_state[k]+1,) + in_state[k+1:]
                if not self.states.bounding_condition(out_state):
                    ind = self.states.index_of(out_state)
                    row[i] = ind
                    p = sum(in_state[:k])
                    data[i]=(-1)**p * (out_state[k])**0.5
            a_k_dag = coo_matrix((data, (row, col)), shape=(self.states.dimension , self.states.dimension), dtype = complex)
            a_k_dag.eliminate_zeros()
            self.a_dag.append(a_k_dag.tocsc())
            
    def vac(self):
        state = np.zeros(self.states.dimension, dtype = complex)
        state[0] = 1.0
        return state
            
class spins:
    def __init__(self, j, states):
        self.states = states
        self.j = j

        more_than_2j = bounding_condition.more_than_n_occupied(2 * j)
        
        #
        self.zero = coo_matrix((self.states.dimension , self.states.dimension), dtype = complex).tocsc()      
        
        #
        self.eye = scipy.sparse.eye(self.states.dimension).tocsc()
        
        #
        self.j_m = []
        for k in range(self.states.num_modes):
            row = np.zeros(self.states.dimension)
            col = np.arange(self.states.dimension, dtype=int)
            data = np.zeros(self.states.dimension)
            for i in range(self.states.dimension):
                in_state = self.states.all_states[i]
                if not in_state[k] == 0:
                    out_state = in_state[:k] + (in_state[k]-1,) + in_state[k+1:]
                    ind = self.states.index_of(out_state)
                    row[i] = ind
                    m = in_state[k] - self.j
                    data[i]= (self.j * (self.j + 1) - m * (m - 1))**0.5
            j_m_k = coo_matrix((data, (row, col)), shape=(self.states.dimension , self.states.dimension), dtype = complex)
            j_m_k.eliminate_zeros()
            self.j_m.append(j_m_k.tocsc())
        
        #
        self.j_p = []
        for k in range(self.states.num_modes):
            row = np.zeros(self.states.dimension)
            col = np.arange(self.states.dimension, dtype=int)
            data = np.zeros(self.states.dimension)
            for i in range(self.states.dimension):
                in_state = self.states.all_states[i]
                if more_than_2j(in_state):
                    raise ValueError("Using more than 2j occupied states to construct spin j operators")
                out_state = in_state[:k] + (in_state[k]+1,) + in_state[k+1:]
                if not self.states.bounding_condition(out_state):
                    ind = self.states.index_of(out_state)
                    row[i] = ind
                    m = in_state[k] - self.j
                    data[i]=(self.j * (self.j + 1) - m * (m + 1))**0.5
            j_p_k = coo_matrix((data, (row, col)), shape=(self.states.dimension , self.states.dimension), dtype = complex)
            j_p_k.eliminate_zeros()
            self.j_p.append(j_p_k.tocsc())
            
        #
        self.j_x = []
        self.j_y = []
        for k in range(self.states.num_modes):
            self.j_x.append((self.j_p[k] + self.j_m[k]) / 2)
            self.j_y.append((self.j_p[k] - self.j_m[k]) / 2 / 1j)
            
        #
        self.j_z = []
        for k in range(self.states.num_modes):
            row = np.zeros(self.states.dimension)
            col = np.arange(self.states.dimension, dtype=int)
            data = np.zeros(self.states.dimension)
            for i in range(self.states.dimension):
                in_state = self.states.all_states[i]
                ind = self.states.index_of(in_state)
                row[i] = ind
                m = in_state[k] - self.j
                data[i] = m
            j_z_k = coo_matrix((data, (row, col)), shape=(self.states.dimension , self.states.dimension), dtype = complex)
            j_z_k.eliminate_zeros()
            self.j_z.append(j_z_k.tocsc())
    def vac(self):
        state = np.zeros(self.states.dimension, dtype = complex)
        state[0] = 1.0
        return state