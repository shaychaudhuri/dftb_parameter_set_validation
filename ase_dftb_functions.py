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
    
    
