import pickle
import numpy as np

with open("data/youcookii/youcookii_data.no_transcript.pickle", 'rb') as infile:
    data = pickle.load(infile)
    for k, v in data.items():
        data[k]["start"] = np.array([])
        data[k]["end"] = np.array([])
        data[k]["text"] = np.array([])

with open("data/youcookii/youcookii_data_no_captions.no_transcript.pickle", 'wb') as outfile:
    pickle.dump(data, outfile)

print()