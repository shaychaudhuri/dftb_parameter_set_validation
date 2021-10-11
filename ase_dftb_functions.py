from ase import Atoms
from ase.calculators.dftb import Dftb
from ase.data import chemical_symbols
import numpy as np
import os

## Kelvin-Hartree conversion factor
K2Ha = 0.316681534524639E-05
