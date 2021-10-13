# DFTB Parameter Set Validation
Repository to validate DFTB+ parameter sets against DFT calculations

Installation instructions:
1. Install [ASE](https://gitlab.com/ase/ase) and set all appropriate paths
2. Compile [DFTB+](https://github.com/dftbplus/dftbplus) with MPI-parallelism and MBD support enabled in `config.cmake`
3. Set `$ASE_DFTB_COMMAND` in your `~/.bashrc` file i.e. `export ASE_DFTB_COMMAND='/path/to/dftb+ > dftb.out`
