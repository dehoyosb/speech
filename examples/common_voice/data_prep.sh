#!/bin/bash

common_voice_path=$1
usage_percentage=$2
python preprocess.py $common_voice_path $usage_percentage
#ln -s $common_voice_path data
