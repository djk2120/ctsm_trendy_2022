#!/bin/bash
casedir='/glade/u/home/djk2120/ctsm_trendy_2022/sims/'
exp='S1'
caseroot=$casedir'TRENDY2022_f09_'$exp

#running from 1851-2021
cd $caseroot
./xmlchange STOP_N=86
cp user_nl_clm.1851-2021 user_nl_clm  #adding transient pop dens


