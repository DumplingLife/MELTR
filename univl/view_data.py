import pickle

with open("data/youcookii/youcookii_data.no_transcript.pickle", 'rb') as file:
    data = pickle.load(file)
with open("data/youcookii/youcookii_videos_features.pickle", 'rb') as file:
    features = pickle.load(file)

print(data)

# zuDJIPoSl7o