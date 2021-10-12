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
    
    Hamiltonian_SlaterKosterFiles_Prefix = '/dev/null',
    Hamiltonian_MaxAngularMomentum_ = '',
    
    kpts = (16,16,1) if (atoms.get_pbc() == [True, True, True]).all() else None,
    
    # Dispersion settings
    Hamiltonian_Dispersion_ = 'MBD',
    Hamiltonian_Dispersion_KGrid = '1 1 1',
    Hamiltonian_Dispersion_Beta = 0.95,
    
    # Analysis settings
    Analysis_ = '',
    Analysis_CalculateForces = 'YES',
    
    # Options
    Options_ = '',
    Options_WriteResultsTag = 'YES',
    Options_WriteDetailedOut = 'YES',
    Options_WriteChargesAsText = 'YES',
    Options_TimingVerbosity = -1)
  
  # Set maximal azimuthal quantum numbers
  set_max_angular_momenta(calc, atoms)
  
  return calc
    
## Define DFTB+ single-point calculator
def dftb_opt_calc(atoms):
  calc = Dftb(
    Driver_ = '',
    
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
    
    Hamiltonian_SlaterKosterFiles_Prefix = '/dev/null',
    Hamiltonian_MaxAngularMomentum_ = '',
    
    kpts = (16,16,1) if (atoms.get_pbc() == [True, True, True]).all() else None,
    
    # Analysis settings
    Analysis_ = '',
    Analysis_CalculateForces = 'YES',
    
    # Options
    Options_ = '',
    Options_WriteResultsTag = 'YES',
    Options_WriteDetailedOut = 'YES',
    Options_WriteChargesAsText = 'YES',
    Options_TimingVerbosity = -1)
  
  # Set maximal azimuthal quantum numbers
  set_max_angular_momenta(calc, atoms)
  
  return calc

def set_max_angular_momenta(calc, atoms):
  max_ls = {'H': '"s"', 'C': '"p"', 'N': '"p"', 'O': '"p"', 'Au': '"d"'}
  sym = [chemical_symbols[i] for i in np.unique(atoms.get_atomic_numbers())]
  settings = {f'Hamiltonian_MaxAngularMomentum_{s}': max_ls[s] for s in sym}
  calc.parameters.update(settings)
