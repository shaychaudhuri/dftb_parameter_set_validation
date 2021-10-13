from ase import Atoms
from ase.db import connect
from ase.io import read
import numpy as np
import os

parameter_set = ''

aims_db = connect("FHIaims.db")
dftb_db = connect(f"{parameter_set}.db")
dftb_sp_db = connect(f"{parameter_set}_SP.db")

size = len(dftb_db)+1

for i in range(1, size):
