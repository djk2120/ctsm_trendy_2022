for f in *CRUNCEP*; do
    echo $f
    
    olddir='/glade/scratch/djk2120/ctsm_trendy_2021/forcing/three_stream'
    newdir='/glade/scratch/djk2120/trendy2022/three_stream'
    sed -i 's:'$olddir':'$newdir':g' $f

    olddom='domain.crujra_v2.2_0.5x0.5.c210804.nc'
    newdom='domain.crujra_v2.3_0.5x0.5.c220801.nc'
    sed -i 's:'$olddom':'$newdom':g' $f
    
    olddat='c2021'
    newdat='c2022'
    sed -i 's:'$olddat':'$newdat':g' $f

    
done