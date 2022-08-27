#!/bin/bash

cimeroot='/glade/work/djk2120/trendy2022/cime/scripts/'
trendy='/glade/u/home/djk2120/ctsm_trendy_2022/'

compset='I1850Clm50BgcCropCru'
res='f09_g17'
project='P93300641'



casedir='/glade/u/home/djk2120/ctsm_trendy_2022/sims/'
caseroot=$casedir'TRENDY2022_f09_spinAD'


cd $cimeroot
./create_newcase --case $caseroot --compset $compset  --res $res --project $project

cd $caseroot
./xmlchange CLM_ACCELERATED_SPINUP="on"
./xmlchange NTASKS_CPL=2520
./xmlchange NTASKS_LND=2520 
./xmlchange NTASKS_ICE=2520 
./xmlchange NTASKS_OCN=2520 
./xmlchange NTASKS_ROF=2520
./xmlchange NTASKS_GLC=2520
./xmlchange NTASKS_WAV=2520
./xmlchange JOB_QUEUE="regular"
./xmlchange JOB_WALLCLOCK_TIME="12:00:00"
./xmlchange PROJECT="P93300641"
./xmlchange RUN_STARTDATE="0000-01-01"
./xmlchange STOP_OPTION="nyears"
./xmlchange STOP_N=100
./xmlchange RESUBMIT=5
./xmlchange DOUT_S=TRUE

./case.setup
cp $trendy'user_datm.streams/PI/user_datm.streams'* ./
cp $trendy'namelists/spinAD/user_nl'* ./

./case.build
./case.submit
