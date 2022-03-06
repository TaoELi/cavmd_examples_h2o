#!/bin/bash

# This script submit all necessary jobs accordingly

for freq in 4150 3950 3650 3550 3450 3350 3150 2750 2500
do
    DIR=Freq_$freq
    mkdir $DIR
    cp data.lmp in.lmp init.xyz input_equlibrate.xml input_traj.xml.bak photon_params.json diabatical_run.sh $DIR
    cd $DIR
    echo "move in $DIR"
    sed -i "s/3550/$freq/" photon_params.json
    sed -i "s/Freq=1000/Freq=$freq/" diabatical_run.sh
    
    qsub diabatical_run.sh
    cd ..
done
