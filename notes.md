### September 9, 2022
  - Post-processing
    - [ ] S0


### September 8, 2022
  - Had a mistake in S1
    - wasnt using the CO2 stream until 1850

### September 6, 2022
  - Had a mistake in S2/S3
    - needed ./xmlchange DATM_CLMNCEP_YR_END=2021
    - restage 1901 restarts
      - cp /glade/scratch/djk2120/archive/TRENDY2022_f09_S2/rest/1901-01-01-00000/* ./
    

### September 5, 2022
  - S2 and S3 crash
    - at different points
  - increasing S3 to 100 nodes
    - rm S3 case
    - qcmd -- ./S3.sh
  - nixing the 1860 switchout for both
  - S2 crashed coming out of 1900
    - was not removing .bin files correctly


### September 4, 2022
  - create tx user.datm
  - S2 is broken into 5 parts
    - 1701-1850 (2x75)   S2.sh
    - 1851-1860 (10)     S2_part2.sh
    - 1861-1900 (40)     ...
    - 1901-1960 (60)     ... 
    - 1961-2021 (61)
  - /glade/u/home/djk2120/tether/tether.sh joblist.txt ../../cheyenne.template &> S2_part1.log &
  - S3 is basically identical to S2
    - except for flanduse in the user_nl_clm
  - /glade/u/home/djk2120/tether/tether.sh joblist.txt ../../cheyenne.template &> S3_part1.log &


### September 3, 2022
  - spinup looking good
    - <5% diseq (TOTECOSYSC 1g/m2)
  - running S0:
    - qcmd -- ./S0.sh > S0.log &
  - running S1:
    - qcmd -- ./S1.sh > S1.log &  (creates,builds case)
    - bash mjl.sh   (makes joblist.txt)
    - /glade/u/home/djk2120/tether/tether.sh joblist.txt ../../cheyenne.template &> S1_part1.log &  (initiates 3job sequence)

### September 2, 2022
  - Spinup is probably fine at 600yrs, will let it go overnight to 800
  - testing out S0 and S1 scripts
  
  - S1 is broken up into three parts
    - 100 years           S1.sh
    - 49 years            S1_part2.sh
    - 2x86 years          S1_part3.sh

  - configuring tether for S1
    - /glade/u/home/djk2120/tether/tether.sh joblist.txt ../../cheyenne.template &> S1_part1.log &

### September 1, 2022
  - runs die overnight due to exceeding scratch quota
    - went on an rm rampage
      - deleted an important PPE file
      - oops
  - resubmitted
    - progressing well


### August 31, 2022
  - spinPostAD is progressing
    - <6% diseq after 200 years
    - drift of 0.015 PgC/yr
    - does seem to be spending a lot of time queued
  - preparing S0 scripts
    - scripts/S0.sh
    - recycle 1901-20 climate, 321 years, 1701-2021
    - made the executive decision to run from 1701, makes way more sense
    - probably will pickup from year 300 of postAD
  - preparing S1 scripts
    - uses a transient compset
      - double-check datm_in that taxmode='cycle'
    - preparing co2 timeseries
  - **spun up with the wrong co2**
    - accidentally used clm default 284.7
    - switched to TRENDY PI at postAD year300
      - ./xmlchange CLM_BLDNML_OPTS="-bgc bgc -crop -co2_ppmv 276.65"
      - easier to use ./xmlchange CCSM_CO2_PPMV="276.65"
    - resubmitted
    

### August 29, 2022
 - spinAD has progressed 600 years
   - ~10% diseq at 1g/m2 (TOTECOSYSC)
   - drift = -0.05 PgC/yr
 - setting up postAD
   - postad.sh
   - qcmd -- ./postad.sh > postad.log &

### August 27, 2022
 - Erik and Peter generated fsurdat, flanduse
 - performed fresh CLM checkout
   - checkout.sh
   - branch_tags/TRENDY-2019.n05_ctsm1.0.dev056
 - configured and submitted spinAD
   - spinad.sh
   - namelists/spinad
 - setting up git version control
 - next up:
   - monitor spinup progress
   - configure spinPostAD


### August 2, 2022
 - Sean converted the input data to three stream
 - downloading ndep data from ftp site
 - converting ndep to CLM format via ndep.ipynb
 - edit user_datm.streams to point to the new files
   - also added direct/diffuse to solar
   - user_datm.streams/PI
