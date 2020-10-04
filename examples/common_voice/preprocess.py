from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import collections
import glob
import json
import os
import random
import pandas as pd

from tqdm import tqdm

from speech.utils import data_helpers
from speech.utils import wave

from phonemizer import phonemize
from phonemizer.separator import default_separator, Separator

WAV_EXT = "wav" # using wv since NIST took wav

def load_phone_map():
    with open("phones.60-48-39.map", 'r') as fid:
        lines = (l.strip().split() for l in fid)
        lines = [l for l in lines if len(l) == 3]
    m60_48 = {l[0] : l[1] for l in lines}
    m48_39 = {l[1] : l[2] for l in lines}
    return m60_48, m48_39

def load_transcripts(path: str, split:str, use_percentage: float) -> dict:
    dataset = pd.read_csv(os.path.join(path, "{}.tsv".format(split)), sep='\t')
    length = len(dataset)
    m60_48, _ = load_phone_map()
    data = {}
    for file_name, text in tqdm(dataset[['path','sentence']].values[:int(use_percentage*(length))]):
        phn = phonemize(text = text.encode('ascii', 'ignore').decode('ascii'), 
                        language='en-us',
                        backend='festival',
                        separator=phone_separator).split()
        phonemes = [m60_48[p] for p in phn if p in m60_48]
        data[os.path.join(path,'clips',file_name)] = phonemes
    return data

def split_by_speaker(data, dev_speakers=50):

    def speaker_id(f):
        return os.path.basename(os.path.dirname(f))

    speaker_dict = collections.defaultdict(list)
    for k, v in data.items():
        speaker_dict[speaker_id(k)].append((k, v))
    speakers = speaker_dict.keys()
    for t in TEST_SPEAKERS:
        speakers.remove(t)
    random.shuffle(speakers)
    dev = speakers[:dev_speakers]
    dev = dict(v for s in dev for v in speaker_dict[s])
    test = dict(v for s in TEST_SPEAKERS for v in speaker_dict[s])
    return dev, test

def convert_to_wav(path):
    data_helpers.convert_full_set(path, "*.mp3",
                                  new_ext=WAV_EXT,
                                  use_avconv=False)

def build_json(data, path, set_name):
    basename = set_name + os.path.extsep + "json"
    with open(os.path.join(path, basename), 'w') as fid:
        for k, t in tqdm(data.items()):
            wave_file = os.path.splitext(k)[0] + os.path.extsep + WAV_EXT
            dur = wave.wav_duration(wave_file)
            datum = {'text' : t,
                     'duration' : dur,
                     'audio' : wave_file}
            json.dump(datum, fid)
            fid.write("\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description="Preprocess Common Voice dataset.")
    parser.add_argument("output_directory",
        help="Path where the dataset is saved.",
        #type = str
        )
    parser.add_argument("--use_percentage",
        help="Data percentage to use.",
        type = float,
        default=1.0
        )
    args = parser.parse_args()

    #TODO: implement data split by speaker
    #TODO: implement run assuming full dataset in folder and take a portion of it

    phone_separator = Separator(phone=' ', syllable='', word='')

    path = os.path.abspath(args.output_directory)

    print("Converting files from mp3 to standard wave format...")
    #convert_to_wav(os.path.join(path, "clips"))

    print("Preprocessing train --> generating phonems from transcripts")
    train = load_transcripts(path, "train", args.use_percentage)
    print("Preprocessing train --> generating training jsons")
    build_json(train, path, "train")

    print("Preprocessing dev --> generating phonems from transcripts")
    dev = load_transcripts(path, "dev", args.use_percentage)
    print("Preprocessing dev --> generating training jsons")
    #dev, test = split_by_speaker(transcripts)
    build_json(dev, path, "dev")

    print("Preprocessing test --> generating phonems from transcripts")
    test = load_transcripts(path, "test", args.use_percentage)
    print("Preprocessing test --> generating training jsons")
    build_json(test, path, "test")
