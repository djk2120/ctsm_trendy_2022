#!/bin/bash
cimeroot='/glade/work/djk2120/trendy2022/cime/scripts/'
trendy='/glade/u/home/djk2120/ctsm_trendy_2022/'
compset='I1850Clm50BgcCropCru'
res='f09_g17'
project='P08010000'
casedir='/glade/u/home/djk2120/ctsm_trendy_2022/sims/'
caseroot=$casedir'TRENDY2022_f09_spinAD_co2'

#need python 3.7.9 for cime
module load python
ncarenv
ncar_pylib


cd $cimeroot
./create_newcase --case $caseroot --compset $compset  --res $res --project $project

cd $caseroot
./xmlchange CLM_ACCELERATED_SPINUP="on"
./xmlchange RUN_TYPE="hybrid"
./xmlchange RUN_REFCASE="TRENDY2022_f09_spinPostAD"
./xmlchange RUN_REFDIR="/glade/scratch/djk2120/archive/TRENDY2022_f09_spinPostAD/rest/0300-01-01-00000"
./xmlchange RUN_REFDATE="0300-01-01"
./xmlchange GET_REFCASE=TRUE
./xmlchange JOB_QUEUE="regular"
./xmlchange JOB_WALLCLOCK_TIME="12:00:00"
./xmlchange PROJECT=$project
./xmlchange RUN_STARTDATE="0000-01-01"
./xmlchange STOP_OPTION="nyears"
./xmlchange STOP_N=60
./xmlchange RESUBMIT=4
./xmlchange DOUT_S=TRUE
./xmlchange CLM_BLDNML_OPTS="-bgc bgc -crop -co2_ppmv 276.65"

./case.setup
cp $trendy'scripts/user_datm.streams/PI/user_datm.streams'* ./
cp $trendy'scripts/namelists/spinAD/user_nl'* ./

./case.build
./case.submit
