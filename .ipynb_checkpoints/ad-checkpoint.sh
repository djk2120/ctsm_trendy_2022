#!/bin/bash

clonecase='/glade/u/home/djk2120/ctsm_trendy_2021/sims/TRENDY2021_f09_spinAD'
casename='TRENDY2022_f09_SpinAD'
trendy='/glade/u/home/djk2120/ctsm_trendy_2022/'
caseroot=$trendy'/sims/'$casename
cimeroot='/glade/work/djk2120/trendy2021/cime/scripts/'



cd $cimeroot

rm -r $caseroot
rm -r "/glade/scratch/djk2120/"$casename
./create_clone --case $caseroot --clone $clonecase --cime-output-root /glade/scratch/djk2120

cd $caseroot



./xmlchange NTASKS_CPL=2520
./xmlchange NTASKS_LND=2520 
./xmlchange NTASKS_ICE=2520 
./xmlchange NTASKS_OCN=2520 
./xmlchange NTASKS_ROF=2520
./xmlchange NTASKS_GLC=2520
./xmlchange NTASKS_WAV=2520
./xmlchange CLM_ACCELERATED_SPINUP=on
./case.setup --reset



cp $trendy'user_datm.streams/PI/user_datm.streams'* ./
cp $trendy'namelists/clm_spinAD' ./user_nl_clm

./xmlchange JOB_QUEUE="regular"
./xmlchange JOB_WALLCLOCK_TIME="12:00:00"
./xmlchange PROJECT="P93300641"
./xmlchange RUN_TYPE=hybrid
./xmlchange RUN_STARTDATE="0000-01-01"
./xmlchange CONTINUE_RUN=FALSE
./xmlchange STOP_OPTION="nyears"
./xmlchange STOP_N=100
./xmlchange RESUBMIT=1
./xmlchange DOUT_S=TRUE
./xmlchange RUN_REFCASE=TRENDY2022_f09_SpinPostAD
./xmlchange RUN_REFDATE=1250-01-01
./xmlchange RUN_REFDIR=/glade/scratch/djk2120/archive/TRENDY2022_f09_SpinPostAD/rest/1250-01-01-00000
./xmlchange GET_REFCASE=TRUE


./case.build --skip-provenance-check
./case.submit
