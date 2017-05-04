#!/bin/bash

cd /export/b14/jlai/spoken/

for filename in /export/b14/jlai/spoken/noise/combined_data/*; do
    echo $(basename $filename .wav) $filename 
done > /export/b14/jlai/spoken/data/train/train-clean-100-wav.scp
