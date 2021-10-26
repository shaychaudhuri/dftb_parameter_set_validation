from ase import Atoms
from ase.db import connect
from ase.io import read
from math import sqrt
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
    
    MSD = 0
    for j in range(len(dft_positions)):
        MSD += (dftb_positions[j][0]-dft_positions[j][0])**2 + (dftb_positions[j][1]-dft_positions[j][1])**2 + (dftb_positions[j][2]-dft_positions[j][2])**2
    MSD /= len(dft_positions)
    RMSD = sqrt(MSD)

    file = open('rmsd.dat', 'a')
    file.write(f'{aims_db[i].data.name} \t {RMSD} \n')
    file.close()

file = np.loadtxt("rmsd.dat", 'a')
plt.title(f'{parameter_set}')

plt.ylabel('Root-Mean-Square Deviation (Å)', fontsize=12)
plt.yticks(fontsize=12)

x, width = np.arange(len(file[:,0])), 0.5
plt.xlim([-width-0.5, len(file[:,0])+0.2])

plt.bar(x, [float(i) for i in file[:,1]], width=width, color='sandybrown')
plt.xticks([])

average = np.mean([float(i) for i in file[:,1]], axis=0)
std = np.std([float(i) for i in file[:,1]], axis=0)

plt.text(x[-30], 2.0, f'Mean average, $\mu$: {np.round(average,3)} Å\nStandard deviation, $\sigma$: {np.round(std,3)} Å')

#for i in range(len(file[:,0])):
#    plt.annotate(file[i,0], xy=(x[i], float(file[i,1]))), rotation=90, fontsize=8)

plt.tight_layout()
plt.savefig('RMSD.png')
plt.show()
