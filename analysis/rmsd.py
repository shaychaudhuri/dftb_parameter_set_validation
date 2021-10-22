from ase import Atoms
from ase.db import connect
from ase.io import read
import matplotlib.pyplot as plt
import numpy as np

parameter_set = ''

aims_db = connect('/path/to/FHIaims_database.db')
dftb_db = connect(f'{parameter_set}.db')

size = len(dftb_db)+1

dict = {'CH':'Methylidyne', 'CN':'Cyanide', 'CO':'Carbon_Monoxide', 'NO':'Nitric_Oxide'}
orientation = ['top', 'bottom']

for i in range(1, size):
    name = aims_db[i].data.name
    dft_atoms = read('/path/to/FHIaims_database.db@'+str(i-1))
    dft_positions = dft_atoms.get_positions()
    
    dftb_atoms = read(str(parameter_set)+'.db@'+str(i-1))
    dftb_positions = dftb_atoms.get_positions()
    
    RMSD = np.average([(np.linalg.norm(dftb_positions[j]-dft_positions[j])**2) for j in range(len(dft_positions))])
