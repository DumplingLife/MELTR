import pickle
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--start', type=int)
parser.add_argument('--end', type=int)

args = parser.parse_args()

with open("data/youcookii/youcookii_data.no_transcript.pickle", 'rb') as infile:
    data = pickle.load(infile)
    for k, v in data.items():
        data[k]["start"] = np.array([args.start])
        data[k]["end"] = np.array([args.end])
        data[k]["text"] = np.array(["cut"]) # use a real word to be safe

with open("data/youcookii/youcookii_data_no_captions.no_transcript.pickle", 'wb') as outfile:
    pickle.dump(data, outfile)

print()