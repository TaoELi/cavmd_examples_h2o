# Quantum CavMD simulations for liquid water under VSC

The folders here contain all necessary files to generate figures in the following paper:

- Li, T. E., Nitzan, A., Hammes-Schiffer, S., Subotnik, J. E., &  (2022). Quantum Simulations of Vibrational Strong Coupling via Path Integrals. arXiv.

## File structure
  - **plotting/** Enter this folder; try *python plot_IR.py* to obtain the IR figure; try *python plot_dielectric.py* to obtain the dielectric constant figure. The raw data for directly plotting the figures are also available in this repo.

  - **collect_all_data_N.py**: Using the command *python collect_all_data_N.py h2o_incav_classical/IR_calculation/Freq_3550/* will generate dipole auto-correlation function of liquid water from all the **simu*xc.xyz** files in the path. The dipole auto-correlation function info will be stored at files **simu*xc.xyz.dac.txt**, which will be directly used for plotting.

  - **get_dielectric.sh**: Using the command *./get_dielectric.sh h2o_incav_classical/dielectric_constant/Freq_3550/* will generate the dielectric constant info in the path. This bash script will call **get_mean_square.py** and **get_mean_value.py** (in the same folder as the bash script) to calculate the square average and the average value of the static dipole moment for each trajectory. This bash script will generate two files (*meansquare_dipole.txt* and *mean_dipole.txt*) in the path, which will be directly used for plotting.

  - **h2o_incav_classical/**
    - **IR_calculation/**

      - **diabatical_run.sh**: A template for submitting a PBS job of CavMD to the server. This template will submit the job to nodes=n15:ppn=1 (node n15 with 1 cpu). The simulation data will be written in **Global_path** (a bash variable defined in this script). If the readers have access to Joe Subotnik's group server **diabatical**,  they probably can completely reproduce the whole work by changing only the **Global_path** to their specified one.

      - **submit_jobs_incav.sh**: Running the command *./submit_jobs_incav.sh* will submit the inside-cavity job, where all the files generated by the code will be temporarily stored at **Global_path** (see above). A 150 ps NVT equilibrium simulation + 40 trajectories of 40 ps NVE simulations will be performed by this script.

      - **submit_jobs_outcav.sh**: A similar file as **submit_jobs_incav.sh** but will submit a outside-cavity job (by setting the light-matter coupling to zero).

      - **other files**: Other files, including (1) *data.lmp*, (2) *init.xyz*, (3) *in.lmp*, (4) *input_equlibrate.xml* or *input_traj.xml.bak*, and (5) *photon_params.json* are input files for performing a series of CavMD simulations with i-PI + LAMMPS (see also https://github.com/TaoELi/cavity-md-ipi/tree/master/tutorials for details of the simulation).

      - **Freq_3550/**: Automatically generated by *submit_jobs_incav.sh*, also storing the raw data for dipole autocorrelation function (**simu_*.xc.xyz.dac.txt**), which can be directly used during plotting. These raw data can be generated by the script *collect_all_data_N.py* (see also https://github.com/TaoELi/cavity-md-ipi/tree/master/tutorials) by using the command *python collect_all_data_N.py Freq_3550/*.

      - **Freq_outcav/**: similar as above.

    - **dielectric_constant/**: The file structure is very similar to  that in **IR_calculation/**. In this job, after a 150 ps equilibrium simulation, 1000 trajectories of 20 ps simulations will be performed (in total 20 ns). Because only the dipole moment info is needed, here the xyz files are not written to the disk, and the dipole moment info will be printed to files named **log_*** in path such as "dielectric_constant/Freq_3550/". The files **log_*** will serve as the input files when the bash script **get_dielectric.sh** is used.

  - **h2o_incav_quantum/**: The file structure is very similar to that in **h2o_incav_classical/**.

    - **IR_calculation/**: Compared with the classical simulation, the only difference is that the job will be run with 32 CPUs (in node n15) by parallel, because a path-integral calculation requires 32 beads.

    - **dielectric_constant/**: Compared with the classical simulation, the only difference is that the job will be run with 32 CPUs  by parallel, because a path-integral calculation requires 32 beads. The inside-cavity job will be submitted to node 12, while the outside-cavity job will be submitted to node 14. **CAUTION: The dielectric constant simulation needs to run for 20 ns, so it is not efficient in the current implementation of CavMD (i-PI + LAMMPS). My personal experience is that several months are needed for the path-integral simulation!**