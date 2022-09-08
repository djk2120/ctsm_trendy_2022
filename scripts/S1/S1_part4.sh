#!/bin/bash
casedir='/glade/u/home/djk2120/ctsm_trendy_2022/sims/'
exp='S1'
caseroot=$casedir'TRENDY2022_f09_'$exp

#running from 1851-2021
cd $caseroot
./xmlchange STOP_N=85



