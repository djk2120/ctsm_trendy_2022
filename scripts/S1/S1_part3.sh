#!/bin/bash
casedir='/glade/u/home/djk2120/ctsm_trendy_2022/sims/'
exp='S1'
caseroot=$casedir'TRENDY2022_f09_'$exp

#running from 1850-2021
cd $caseroot
./xmlchange STOP_N=1 #86
./xmlchange RESUBMIT=1 
cp user_nl_clm.1850-2021 user_nl_clm


