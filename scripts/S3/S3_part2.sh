#!/bin/bash

## run the next 10 years of S3 (1851-1860)
## switching over to transient aerosol,urban,popdens
## running only ten years to keep datm aligned
##    using 1911-1920 forcing

casedir='/glade/u/home/djk2120/ctsm_trendy_2022/sims/'
exp='S3'
casename='TRENDY2022_f09_'$exp
caseroot=$casedir$casename

cd $caseroot
./xmlchange STOP_N=10

cp user_nl_clm.1851-2021 user_nl_clm
cp user_nl_datm.1851-1860 user_nl_datm

cd '/glade/scratch/djk2120/'$caseroot'/run'
rm *.bin

cd $caseroot

