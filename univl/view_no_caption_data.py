import pickle

with open("data/youcookii/youcookii_data.no_transcript.pickle", 'rb') as file:
    print(pickle.load(file))