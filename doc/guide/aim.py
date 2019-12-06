from pytriqs.gf import *
from pytriqs.operators import *
from pytriqs.archive import *
from nrgljubljana_interface import Solver, FlatNew

# Parameters
D, V, U = 1.0, 0.25, 1.0
e_f, beta = -U/2.0, 10000
T = 1.0/beta

# Set up the Solver
S = Solver(model = "SIAM", symtype = "QS", mesh_max = 2.0, mesh_min = 1e-4, mesh_ratio = 1.01)

# Solve Parameters
sp = {}
sp["T"] = T
sp["Lambda"] = 2.0
sp["Nz"] = 2
sp["Tmin"] = 1e-5
sp["keep"] = 1000
sp["keepenergy"] = 10.0

# Model Parameters
mp = {}
mp["U1"] = U
mp["eps1"] = e_f
sp["model_parameters"] = mp

# Low-level NRG Parameters
np = {}
np["bandrescale"] = 1.0
S.set_nrg_params(**np)

# Initialize hybridization function
S.Delta_w['imp'] << V**2 * FlatNew(D)

# Solve the impurity model
S.solve(**sp)

# Store the Result
with HDFArchive("aim_solution.h5", 'w') as arch:
    arch["A_w"] = S.A_w
    arch["G_w"] = S.G_w
    arch["F_w"] = S.F_w
    arch["Sigma_w"] = S.Sigma_w
    arch["expv"] = S.expv

print("<n>=", S.expv["n_d"])
