# CavMD Files for liquid water under VSC

All the necessary input or post-processing files for reproducing the following publications:

**water_VUSC/**

- Li, T. E., Subotnik, J. E., Nitzan, A. Cavity molecular dynamics simulations of liquid water under vibrational ultrastrong coupling. [Proc. Natl. Acad. Sci., 2020, 117(31), 18324–18331](https://doi.org/10.1073/pnas.2009272117).

**water_trpmd/**

- Li, T. E., Nitzan, A., Hammes-Schiffer, S., Subotnik, J. E. Quantum Simulations of Vibrational Strong Coupling via Path Integrals. 	[arXiv:2203.03001, 2022](https://arxiv.org/abs/2203.03001).

I strongly recommend the readers to try reproducing **water_trpmd/** instead of **water_VUSC/** due to the cleaner file structure and documentation. Note that **water_trpmd/** also contains the classical simulation.

The source code of CavMD and installation tutorials are stored in https://github.com/TaoELi/cavity-md-ipi.

Note that all plotting scripts in the folders above need a wrapper code (**import columnplots as clp**) in https://github.com/TaoELi/columnplots.
