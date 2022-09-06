#!/bin/bash
## run the next 60 years of S2 (1901-1960)
## bring in transient climate
casedir='/glade/u/home/djk2120/ctsm_trendy_2022/sims/'
exp='S2'
casename='TRENDY2022_f09_'$exp
caseroot=$casedir$casename

cd $caseroot
./xmlchange STOP_N=60
#need python 3.7.9 for cime
module load python
module load ncarenv
ncar_pylib

cp user_nl_datm.1901-2021 user_nl_datm
cd '/glade/scratch/djk2120/'$caseroot'/run'
rm *.bin

cd $caseroot

./case.setup --reset
./case.build --clean

