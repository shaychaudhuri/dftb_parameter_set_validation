from ase import Atoms
from ase.db import connect
from ase.io import read
import matplotlib.pyplot as plt
import numpy as np
import os

parameter_set = ''

aims_db = connect("FHIaims.db")
dftb_db = connect(f"{parameter_set}.db")
dftb_sp_db = connect(f"../{parameter_set}_SP/{parameter_set}_SP.db")

size = len(dftb_db)+1

dict = {'CH':'Methylidyne', 'CN':'Cyanide', 'CO':'Carbon_Monoxide', 'NO':'Nitric_Oxide'}
orientation = ['top', 'bottom']

for i in range(1, size):
    ###########################
    ## DFT adsorption energy ##
    ###########################
    name = aims_db[i].data.name
    if '@' not in name:
        continue
    else:
        combined = name
        substrate = name.split("@")[1]
        adsorbate = name.split("@")[0]
        
        ## Get combined system energy
        combined_file = aims_db[i].data.aims_out.splitlines()
        for line in combined_file:
            if "Total energy corr" in line:
                linesplit = line.split()
                combined_energy_dft = float(linesplit[-2])
                
        for j in range(1, size):
            ## Get substrate energy
            if substrate == aims_db[j].data.name:
                substrate_file = aims_db[j].data.aims_out.splitlines()
                for line in substrate_file:
                    if "Total energy corr" in line:
                        linesplit = line.split()
                        substrate_energy_dft = float(linesplit[-2])
                        
            ## Get adsorbate energy
            if adsorbate == aims_db[j].data.name:
                adsorbate_file = aims_db[j].data.aims_out.splitlines()
                for line in adsorbate_file:
                    if "Total energy corr" in line:
                        linesplit = line.split()
                        adsorbate_energy_dft = float(linesplit[-2])   
            elif adsorbate in [f'{x}_{y}' for y in orientation for x in dict]:
                symbols = adsorbate.split("_")[0]
                adsorbate = dict[symbols]
                if adsorbate == aims_db[j].data.name:
                    adsorbate_file = aims_db[j].data.aims_out.splitlines()
                    for line in adsorbate_file:
                        if "Total energy corr" in line:
                            linesplit = line.split()
                            adsorbate_energy_dft = float(linesplit[-2])
                        
        adsorption_energy_dft = combined_energy_dft - substrate_energy_dft - adsorbate_energy_dft

    ############################    
    ## DFTB adsorption energy ##
    ############################
    name = dftb_db[i].data.name
    if '@' not in name:
        continue
    else:
        combined = name
        substrate = name.split("@")[1]
        adsorbate = name.split("@")[0]
        
        ## Get combined system energy
        combined_file = dftb_db[i].data.dftb_out.splitlines()
        for line in combined_file:
            if "Total Energy:" in line:
                linesplit = line.split()
                combined_energy_dftb = float(linesplit[-2])
                
        for j in range(1, size):
            ## Get substrate energy
            if substrate == dftb_sp_db[j].data.name:
                substrate_file = dftb_sp_db[j].data.dftb_out.splitlines()
                for line in substrate_file:
                    if "Total Energy:" in line:
                        linesplit = line.split()
                        substrate_energy_dftb = float(linesplit[-2])
                        
            ## Get adsorbate energy
            if adsorbate == dftb_sp_db[j].data.name:
                adsorbate_file = dftb_sp_db[j].data.dftb_out.splitlines()
                for line in adsorbate_file:
                    if "Total Energy:" in line:
                        linesplit = line.split()
                        adsorbate_energy_dftb = float(linesplit[-2])   
            elif adsorbate in [f'{x}_{y}' for y in orientation for x in dict]:
                symbols = adsorbate.split("_")[0]
                adsorbate = dict[symbols]
                if adsorbate == dftb_sp_db[j].data.name:
                    adsorbate_file = dftb_sp_db[j].data.dftb_out.splitlines()
                    for line in adsorbate_file:
                        if "Total Energy:" in line:
                            linesplit = line.split()
                            adsorbate_energy_dftb = float(linesplit[-2])
                        
        adsorption_energy_dftb = combined_energy_dftb - substrate_energy_dftb - adsorbate_energy_dftb             

        file = open('adsorption_energies.dat', 'a')
        file.write(f'{name} \t {adsorption_energy_dft} \t {adsorption_energy_dftb} \n')
