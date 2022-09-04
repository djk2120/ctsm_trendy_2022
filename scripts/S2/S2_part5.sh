#!/bin/bash
## final 61 years of S2 (1961-2021)
casedir='/glade/u/home/djk2120/ctsm_trendy_2022/sims/'
exp='S2'
casename='TRENDY2022_f09_'$exp
caseroot=$casedir$casename

cd $caseroot
./xmlchange STOP_N=61

