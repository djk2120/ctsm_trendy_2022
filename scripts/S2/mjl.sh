casedir='/glade/u/home/djk2120/ctsm_trendy_2022/sims/'
exp='S2'
caseroot=$casedir'TRENDY2022_f09_'$exp

d=$(pwd)
helpers=( 'none' $d'/S2_part2.sh' $d'/S2_part3.sh' $d'/S2_part4.sh' $d'/S2_part5.sh' )

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

