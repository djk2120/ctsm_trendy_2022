#!/bin/bash
## run the next 60 years of S3 (1901-1960)
## bring in transient climate
casedir='/glade/u/home/djk2120/ctsm_trendy_2022/sims/'
exp='S3'
casename='TRENDY2022_f09_'$exp
caseroot=$casedir$casename

#need python 3.7.9 for cime
module load python
module load ncarenv
ncar_pylib

cd $caseroot


cp user_nl_datm.1901-2021 user_nl_datm
cd '/glade/scratch/djk2120/'$casename'/run'
rm *.bin

cd $caseroot

