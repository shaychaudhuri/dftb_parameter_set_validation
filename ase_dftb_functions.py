from ase import Atoms
from ase.calculators.dftb import Dftb
from ase.data import chemical_symbols
import numpy as np
import os

## Kelvin-Hartree conversion factor
K2Ha = 0.316681534524639E-05

## Define DFTB+ optimisation calculator
def dftb_opt_calc(atoms):
  calc = Dftb(
    # Driver settings
    Driver_ = 'LBFGS',
    Driver_AppendGeometries = 'YES',
    Driver_LatticeOpt = 'NO',
    Driver_MaxSteps = -1, 
    
    # SCC settings
    Hamiltonian_SCC = 'YES',
    Hamiltonian_MaxSCCIterations = 3000,
    Hamiltonian_SCCTolerance = 1E-5, 
    Hamiltonian_ShellResolvedSCC = 'YES',
    
    # Hamiltonian-specific settings
    Hamiltonian_Filling_ = 'Fermi',
    Hamiltonian_Filling_Temperature = 1160*K2Ha,
    Hamiltonian_Mixer_ = 'Broyden',
    Hamiltonian_Mixer_MixingParameter = 0.01,
    Hamiltonian_Mixer_InverseJacobiWeight = 0.01,
    Hamiltonian_Mixer_MinimalWeight = 1.0,
    Hamiltonian_Mixer_MaximalWeight = 1E5,
    
    Hamiltonian_SlaterKosterFiles_Prefix = 'dev/null',
    Hamiltonian_MaxAngularMomentum_ = '',
    
    kpts = (16,16,1) if (atoms.get_pbc() == [True, True, True]).all() else None,
    
    # Dispersion settings
