#!/bin/bash
## run the next 40 years of S2 (1861-1900)

casedir='/glade/u/home/djk2120/ctsm_trendy_2022/sims/'
exp='S2'
casename='TRENDY2022_f09_'$exp
caseroot=$casedir$casename

cd $caseroot
./xmlchange STOP_N=40

cp user_nl_datm.1861-1900 user_nl_datm
cd '/glade/scratch/djk2120/'$caseroot'/run'
rm *.bin

cd $caseroot

