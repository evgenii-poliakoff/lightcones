# Contents of the notebooks folder

## spin_boson_model.ipynb

In this notebook we consider the model of open quantum system, on the example of spin-boson model.
We discuss how the initial value problem is posed for the nonstationary dynamics of local quantum quench.
We also provide an example of a numerically exact (i.e. converged with respect to truncation parameters)
computation of observable averages via solution of the non-stationary Schrodinger equation in the truncated Fock space.

## star2chain.ipynb

Here we introduce the two standard forms of the open quantum system model: the star and the chain representations, and how to switch between them

## operator_spread.ipynb

In the interacting picture (with respect to the free bath), the coupling operator will spread along the chain during the quench. The coefficients of the spread $\alpha_k\left(t\right)$ play important role in our approach

## wavepackets_decoupling.ipynb

Here we demonstrate why the real-time local quench problem is a complicated many-body problem: there is no backward front in the spatial picture. The emitted quanta decouple very slowly (the commutators decay in an algebraic way). We have long-range interaction in the time domain.

## light_cone_interior_normal_modes.ipynb

Here we discuss the retarded light cone density matrix, the light cone interior normal modes, and their asymptotic properties.

## fidelity_relevant_subspace.ipynb

Here we demonstrate the convergence properties of the fidelity of the full open system-bath wavefunction with respect to the number of kept light cone interior normal modes.

## arrival_times.ipynb

The concept of arrival times (inside the light cone interior) for degress of freedom is illustrated. A sequence of arrival times is defined for arbitrary frame. Different frames have different rates at which the modes arrive. In the star representations all the modes arrive (almost) instantly at $t=0$. Whereas in the chain representations the modes arrive gradually (the light cone is well defined).

## minimal_lighcone.ipynb

There is a frame such that the rate at which the modes arrive is minimal. (Roughly speaking, a frame in which the Lieb-Robinson velocity is minimal). A numerical procedure to construct such a frame is presented.

## backward_lightcone.ipynb

Here we provide the code sample where the backward light cone is superposed on the minimal forward light cone. We call this the "causal diamond" frame. We demonstrate that the dynamics of the driven spin inside the boson bath is correctly reproduced.

## quantum_jumps.ipynb

Here we provide the code sample where the modes which escape the backward light cone are measured via quantum jump Monte Carlo sampling. The jumps are implemented via the Schmidt decomposition of the bipartite system 'escaped mode'+'the rest'.