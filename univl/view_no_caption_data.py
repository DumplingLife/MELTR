import pickle

with open("data/youcookii/youcookii_data_no_captions.no_transcript.pickle", 'rb') as file:
    print(pickle.load(file))