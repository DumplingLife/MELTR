import pickle
import numpy as np

with open("data/youcookii/youcookii_data.no_transcript.pickle", 'rb') as infile:
    data = pickle.load(infile)
    for k, v in data.items():
        # fill it with some stuff
        data[k]["start"] = np.array([20])
        data[k]["end"] = np.array([30])
        data[k]["text"] = np.array(["cut"]) # use a real word to be safe

with open("data/youcookii/youcookii_data_no_captions.no_transcript.pickle", 'wb') as outfile:
    pickle.dump(data, outfile)

print()