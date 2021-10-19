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

## DFTB adsorption energy
for i in range(1, size):
    name = dftb_sp_db[i].data.name
    if '@' not in name:
        continue
    else:
        combined = name
        substrate = name.split("@")[1]
        adsorbate = name.split("@")[0]
        
        ## Get combined system energy
        combined_file = dftb_sp_db[i].data.dftb_out.splitlines()
        for line in combined_file:
            if "Total Energy:" in line:
                linesplit = line.split()
                combined_energy = float(linesplit[-2])
                
        for j in range(1, size):
            ## Get substrate energy
            if substrate == dftb_sp_db[j].data.name:
                substrate_file = dftb_sp_db[j].data.dftb_out.splitlines()
                for line in substrate_file:
                    if "Total Energy:" in line:
                        linesplit = line.split()
                        substrate_energy = float(linesplit[-2])
                        
            ## Get adsorbate energy
            if adsorbate == dftb_sp_db[j].data.name:
                adsorbate_file = dftb_sp_db[j].data.dftb_out.splitlines()
                for line in adsorbate_file:
                    if "Total Energy:" in line:
                        linesplit = line.split()
                        adsorbate_energy = float(linesplit[-2])               
                        
        adsorption_energy = combined_energy - substrate_energy - adsorbate_energy                
