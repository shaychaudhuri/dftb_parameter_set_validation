from ase import Atoms
from ase.db import connect
from ase.io import read
import matplotlib.patches as mpatches
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
        file.write(f'{combined} \t {adsorption_energy_dft} \t {adsorption_energy_dftb} \n')
        
file = np.loadtxt("adsorption_energies.dat", dtype=str)
sub_dict = {'Au10':'Au$_{10}$', 'Au18':'Au$_{18}$', 'Au34':'Au$_{34}$', 'Au111':'Au(111)'}

substrates = list(set([i.split("@")[1] for i in file[:,0]]))
for i in range(len(substrates)):
    ax = plt.figure(i)
    plt.title(sub_dict[substrates[i]], fontsize=14)
    plt.ylabel('Adsorption Energy (eV)', fontsize=12)
    plt.yticks(fontsize=12)
    
    xlabels = []
    for j in file[:,0]:
        if j.split("@")[1] == substrates[i]
            xlabels.append(j.split("@")[0])
            x, width = np.arange(len(xlabels)), 0.35
    for k in range(len(xlabels)):
        if "_" in xlabels[k]:
            xlabels[k] = xlabels[k].replace("_", ' ')
    
    dft_color, dftb_color = 'firebrick', 'sandybrown'
    counter = -1
    
    for l in range(len(file[:,0])+1):
        if file[l,0].split("@")[1] == substrates[i]:
            counter += 1
            plt.bar(counter-width/2, float(file[l,1]), width=width, color=dft_color)
            plt.bar(counter+width/2, float(file[l,2]), width=width, color=dftb_color)
            plt.xticks(x, labels=xlabels, fontsize=10)
            plt.setp(plt.gca().get_xticklabels(), rotation=30, ha='right')
            
     plt.ylim(plt.gca().get_ylim()[::-1])
     
     dft = mpatches.Patch(color=dft_color, label='DFT')
     dftb = mpatches.Patch(color=dftb_color, label=parameter_set)
     plt.legend(handles=[dft, dftb], loc='upper right', prop={'size':12})
      
     plt.savefig(f'Eads_{substrates[i]}.png')
