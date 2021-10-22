from ase import Atoms
from ase.db import connect
from ase.io import read
import matplotlib.pyplot as plt
import numpy as np

parameter_set = ''

aims_db = connect('/path/to/FHIaims_database.db')
dftb_db = connect(f'{parameter_set}.db')

size = len(dftb_db)+1

