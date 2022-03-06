#!/bin/bash

echo "starting dealing with dielectric constant of liquid water"

dir=$1
echo "working under folder $dir"

rm $dir/mean_dipole.txt
rm $dir/meansquare_dipole.txt
touch $dir/mean_dipole.txt
touch $dir/meansquare_dipole.txt

for idx in {1..1000}
do

	filename=$dir/log_$idx
	tmp_file=tmp_$idx

	echo "translating log_$idx"
	cat $filename | grep -i "^mux = " | grep -i " muy = " | grep -i " muz = " | grep -i "\\[units of a.u.\\]" | awk '{print $3 " " $6 " " $9}' | awk '/^[+-]?[0-9]+\.?[0-9]*\s[+-]?[0-9]+\.?[0-9]*\s[+-]?[0-9]+\.?[0-9]*$/' > tmp_$idx
	wait
	echo "calculating mean value"
	mean_value=$(python get_mean_value.py tmp_$idx)
	wait
	echo "calculating mean square value"
	means_value=$(python get_mean_square.py tmp_$idx)
	wait
	n=$(wc -l tmp_$idx | awk '{print $1}')
	wait

	echo "$idx $mean_value $n" >> $dir/mean_dipole.txt
	echo "$idx $means_value $n" >> $dir/meansquare_dipole.txt

	rm tmp_$idx
	wait
done
