from ase.atoms import Atoms
from ase.calculators.dftb import Dftb
from ase.constraints import constrained_indices
from ase.db import connect
from ase.io import read
from ase_dftb_functions import *
import os

## Input name of parameter set
parameter_set = ''

aims_db = connect("FHIaims.db")
dftb_db = connect(f'{parameter_set}_SP.db')

for i in range(len(aims_db)):
    os.mkdir(aims_db[i].data.name)
    os.chdir(aims_db[i].data.name)
  
    ## Run single-point calculation
    atoms = read(f'FHIaims.db@{i-1}')
    dftb_sp = dftb_sp_calc(atoms)
    dftb_sp.set(Hamiltonian_SlaterKosterFiles_Prefix = f"path/to/{parameter_set}/")
      
    dftb_sp.calculate(atoms)
  
    data = {'name': aims_db[i].data.name,
          'dftb_out': open("dftb.out", 'r').read(),
          'dftb_in_hsd': open("dftb_in.hsd", 'r').read(),
          'dftb_pin_hsd': open("dftb_pin.hsd", 'r').read(),
          'band_out': open("band.out", 'r').read(),
          'charges_dat': open("charges.dat", 'r').read(),
          'detailed_out': open("detailed.out", 'r').read()
         }
  
    dftb_db.write(atoms, data=data)
  
    os.chdir('../')
