#!/bin/bash

# This script submit all necessary jobs accordingly

RUN=run_outcav

DIR=Freq_outcav
mkdir $DIR
cp data.lmp in.lmp init.xyz input_equlibrate.xml input_traj.xml.bak photon_params.json diabatical_run_out.sh $DIR
cd $DIR
echo "move in $DIR"

mv diabatical_run_out.sh diabatical_run.sh

sed -i "s/4e-4/0e-4/" photon_params.json
sed -i "s/Freq=1000/Freq=outcav/" diabatical_run.sh

qsub diabatical_run.sh
cd ..
