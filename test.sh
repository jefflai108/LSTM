#!/bin/bash

for filename in /Users/jefflai108/clsp/clsp/*; do 
	#echo $filename
	echo "${filename%.*}" sox filename -t wav \| >> test-wav.scp	
done
