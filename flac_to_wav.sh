#!/bin/bash

cd /export/b14/jlai/spoken/

i=0
for directory in /export/b14/jlai/spoken/flac_data/*; do 
        for sub_direcotry in $directory/*; do
                for filename in $sub_direcotry/*; do
                	sox $filename -t wav flac_to_wav$i.wav
                	((i++))
                done
        done
done