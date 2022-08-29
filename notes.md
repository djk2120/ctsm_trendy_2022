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
