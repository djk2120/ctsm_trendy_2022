#!/bin/bash
casedir='/glade/u/home/djk2120/ctsm_trendy_2022/sims/'
exp='S1'
caseroot=$casedir'TRENDY2022_f09_'$exp

#running from 1801-1849, as previous
cd $caseroot
./xmlchange STOP_N=49

