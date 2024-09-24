import numpy as np
from multiprocessing import Pool, cpu_count

from . import spin_boson_model_ring

def compute_s_z_av_core(n_samples, seed = None):
    _mvf = spin_boson_model_ring.mvf()
    s_z_av_table = _mvf.compute_s_z_av(n_samples, seed)
    return s_z_av_table
    

def compute_s_z_av(n_samples, n_cpu, seed = None):
    
    num_cores = cpu_count()
    if n_cpu > num_cores:
        raise ValueError("Requested number of cpu's ", n_cpu, " is greater than the number of available cpu's ", num_cores)
    
    # Create a list of arguments for each  worker
    if seed is None:
        args_list = [(n_samples, None) for i in range(n_cpu)]
    else:
        args_list = [(n_samples, i + seed) for i in range(n_cpu)]
    
    # Run the parallel computation
    with Pool(processes=n_cpu) as pool:
        results = pool.map(compute_s_z_av_core, args_list)
        
    
    # Sum the result
    s_z_av_table = results[0]
    for r in results[1:]:
        s_z_av_table[:, 1] = s_z_av_table[:, 1] + r[:, 1]
        
    # normalize
    s_z_av_table[:, 1] = s_z_av_table[:, 1] / (n_cpu * n_samples)
    
    return s_z_av_table