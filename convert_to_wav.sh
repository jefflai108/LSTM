#!/bin/bash

#Jeff Lai 
#3/14/2017
#Bash file for converting audio files in /export/a15/vpanayotov/data/LibriSpeech/train-clean-100
#to the same format as /export/b15/janto/kaldi/kaldi/egs/sre10/v1/data/train/wav.scp 
#in order for executing /export/b15/janto/kaldi/kaldi/egs/sre10/v1/run.sh 
#Output to a file called train-clean-100-wav.scp; run on clsp server 

cd /export/b14/jlai/spoken/data/train/

for directory in /export/a15/vpanayotov/data/LibriSpeech/train-clean-100/*; do 
	for sub_direcotry in $directory/*; do 
		for filename in $sub_direcotry/*; do 
				#format: file_basename_1 sox file_1 -t wav |
				#echo "/export/a15/vpanayotov/data/LibriSpeech/train-clean-100/911/128684/911-128684-0074.flac" | cut -d '/' -f 10  
				b=`echo "${filename%.*}" | cut -d '/' -f 10`
				echo $b sox $filename -t wav \| >> train-clean-100-wav.scp
		done
	done
done

