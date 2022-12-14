#!/bin/bash
## run the next 60 years of S2 (1901-1960)
## bring in transient climate
casedir='/glade/u/home/djk2120/ctsm_trendy_2022/sims/'
exp='S2'
casename='TRENDY2022_f09_'$exp
caseroot=$casedir$casename

cd $caseroot
./xmlchange STOP_N=60
cp user_nl_datm.1901-2021 user_nl_datm
./xmlchange DATM_CLMNCEP_YR_END=2021
cd '/glade/scratch/djk2120/'$casename'/run'
rm *.bin

cd $caseroot


