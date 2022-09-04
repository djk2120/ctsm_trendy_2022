
### September 4, 2022
  - create tx user.datm
  - S2 is broken into 5 parts
    - 1701-1800 (100)   S2.sh
    - 1800-1849 (49)    S2_part2.sh
    - 1850-1900 (51)    ...
    - 1901-1960 (60)
    - 1961-2021 (61)

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
