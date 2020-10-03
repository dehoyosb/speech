from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import glob
import os
from tqdm import tqdm

from speech.utils import convert

def convert_full_set(path, pattern, new_ext="wav", **kwargs):
    pattern = os.path.join(path, pattern)
    audio_files = glob.glob(pattern)
    for af in tqdm(audio_files):
        base, ext = os.path.splitext(af)
        wav = base + os.path.extsep + new_ext
        if wav not in os.listdir(path):
            convert.to_wave(af, wav, **kwargs)




