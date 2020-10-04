Example using the Common Voice dataset from Mozilla. It can be downloaded here: https://commonvoice.mozilla.org/en/datasets

The data is mapped from 61 to 48 phonemes for training. For final test set
evaluation the 48 phonemes are again mapped to 39. The phoneme mapping is the
standard recipe, the map used here is taken from the [Kaldi TIMIT recipe].

## Setup

Once you have the Common Voice data downloaded, run

```
./data_prep.sh <path_to_common_voice>
```

This script will convert the `.mp3` to `.wav` files and store them in the same
location. You'll need write access to directory where common_voice is stored. It will
then symlink the timit directory to `./data`. There should be three data json
files in `data/`:

- `train.json`: 
- `dev.json`: 
- `test.json`: 

## Train 

There is a CTC and a sequence-to-sequence with attention configuration. Before
training a model, edit the configuration file. In particular, set the
`save_path` to a location where you'd like to store the model. Edit any other
parameters for your experiment. From the top-level directory, you can train the
model with

``` 
python train.py examples/common_voice/ctc_config.json
```

## Score

Save the 48 phoneme predictions with the top-level `eval.py` script.

```
python eval.py <path_to_model> examples/common_voice/data/test.json --save predictions.json
```

To score using the reduced phoneme set (39 phonemes) run 

```
python examples/common_voice/score.py predictions.json 
```
