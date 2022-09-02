casedir='/glade/u/home/djk2120/ctsm_trendy_2022/sims/'
exp='S1'
caseroot=$casedir'TRENDY2022_f09_'$exp

helpers=( 'none' 'S1_part2.sh' 'S1_part3.sh' )

:>joblist.txt
i=0
for helper in ${helpers[@]}; do
    ((i++))
    s=""
    s=$s$exp"_part"$i","
    s=$s$caseroot","
    s=$s$helper","

    if [ $i -eq 1 ]; then
	s=$s"queued"
    else
	s=$s"waiting"
    fi

    echo $s >> joblist.txt

done

