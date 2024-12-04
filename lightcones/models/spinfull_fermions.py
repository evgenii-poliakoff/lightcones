
import lightcones.space as sp
from lightcones.linalg import kron

class spinfull_fermions:
    def __init__(self, num_modes):
        states = sp.states(num_modes, bounding_condition=sp.bounding_condition.more_than_singly_occupied())
        f = sp.fermions(states)
        
        self.eye = kron(f.eye, f.eye)
        self.parity = kron(f.parity, f.parity)
        
        # ordering is the following:
        # up down
        
        # a and a_dag are odd operators
        self.a = [kron(f.a, f.eye),  kron(f.parity, f.a)]
        self.a_dag = [kron(f.a_dag, f.eye), kron(f.parity, f.a_dag)]
        
        # n is even operator
        self.n = [kron(f.n, f.eye),  kron(f.eye, f.n)]