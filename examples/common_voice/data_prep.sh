#!/bin/bash

common_voice_path=$1
python preprocess.py $common_voice_path
ln -s $common_voice_path data
